from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.views.generic import ListView, View
from django.db.models import OuterRef, Exists, Prefetch
from django.contrib.postgres.aggregates import StringAgg
from .models import my_profile_model
from .forms import NewUserForm, CreateGroupForm, AccountUpdateForm, PasswordChangeForm
from .utils import sys_admin_test
from main.models import User, organization_model, project_list_model, user_project_model

# =============================================================
# Register
# =============================================================

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

# =============================================================
# Logout
# =============================================================

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("main:homepage")

# =============================================================
# Login
# =============================================================

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

# =============================================================
# myProfile
# =============================================================

@login_required
def myProfile(request):
    return render(request, 'user_management/myProfile.html')

# =============================================================
# myProfile - Update
# =============================================================

@login_required
def myProfile_update(request):
    if request.method == 'POST':
        account_form = AccountUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_management:myProfile')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_management:myProfile')
    else:
        account_form = AccountUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'user_management/myProfile.html', {'account_form': account_form, 'password_form': password_form})

# =============================================================
# Password Update
# =============================================================

@login_required
class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

# =============================================================
# Manage Users
# =============================================================

def manage_users(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect unauthorized users

    users = User.objects.all()
    groups = Group.objects.all()
    permissions = Permission.objects.all()

    if request.method == 'POST':
        for user in users:
            group_ids = request.POST.getlist(f'user_{user.id}_groups')
            user.groups.set(group_ids)

            permission_ids = request.POST.getlist(f'user_{user.id}_permissions')
            user.user_permissions.set(permission_ids)
    context = {
        'users': users,
        'groups': groups,
        'permissions': permissions
    }
    return render(request, 'user_management/manage_users.html', context)

# =============================================================
# Create Group
# =============================================================

def create_group(request):
    if request.method == 'POST':
        print('POST request')
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            print('Form is valid')
            group_name = form.cleaned_data['group_name']
            # Create a new group instance
            group = Group.objects.create(name=group_name)
            #group.save()
            # Optionally, add users to the group if selected in the form
            users = form.cleaned_data['users']
            if users:
                group.user_set.set(users)
                print(users)
            # Redirect to a success page or wherever you want after group creation
            return redirect('user_management:manage_users')  # Redirect to the manage users page
    else:
        print("not a post request..")
        form = CreateGroupForm()
    return render(request, 'user_management/create_group.html', {'create_group_form': form})

# =============================================================
# Users
# =============================================================

class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_management/users.html'
    context_object_name = 'users'

    # Query sets for table
    def get_queryset(self):
        authorized_group = Group.objects.get(name='Authorized Tool User')
        admin_group = Group.objects.get(name='System Admin')

        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all())
        ).annotate(
            is_authorized=Exists(authorized_group.user_set.filter(id=OuterRef('id'))),
            is_admin=Exists(admin_group.user_set.filter(id=OuterRef('id'))),
            organizations=StringAgg('organization_users__org_name', delimiter=', ')
        )
        
        return users

    # Fetch context data from the database
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_list'] = self.request.user.favorite_projects.all()
        context['sys_admin'] = sys_admin_test(self.request.user)
        return context

    # Check if user is system admin
    def test_func(self):
        return self.request.user.groups.filter(name='System Admin').exists()
    
    # Redirect to 403 page
    def handle_no_permission(self):
        return render(self.request, 'main/403.html', status=403)
    
# =============================================================
# Users - Update & Delete
# =============================================================

class UserGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    # Check if user is system admin
    def test_func(self):
        return self.request.user.groups.filter(name='System Admin').exists()

    # Redirect to 403 page
    def handle_no_permission(self):
        return render(self.request, 'main/403.html', status=403)

    # Handle POST request
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        authorized_group = Group.objects.get(name='Authorized Tool User')
        admin_group = Group.objects.get(name='System Admin')

        # Delete User check
        if 'delete-user' in request.POST:
            # Delete user
            user.delete()

        # Update User check
        elif 'update-user' in request.POST:
            
            # Authorized User group check
            if 'authorized' in request.POST:
                # Add Authorized Tool User group
                if request.POST['authorized'] == 'on':
                    user.groups.add(authorized_group)
            else:
                # Remove Authorized Tool User group
                user.groups.remove(authorized_group)

            # System Admin group check
            if 'admin' in request.POST:
                # Add System Admin group
                if request.POST['admin'] == 'on':
                    user.groups.add(admin_group)
            else:
                # Remove System Admin group
                user.groups.remove(admin_group)

        return HttpResponseRedirect(reverse('user_management:users'))  # Redirect back to the user list