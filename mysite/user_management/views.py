from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, CreateGroupForm, AccountUpdateForm, PasswordChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django import forms
import platform

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

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("main:homepage")


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

@login_required
def account(request):
    return render(request, 'user_management/account.html')

@login_required
def account_update(request):
    if request.method == 'POST':
        account_form = AccountUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_management:account')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_management:account')
    else:
        account_form = AccountUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'user_management/account_update.html', {'account_form': account_form, 'password_form': password_form})

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
