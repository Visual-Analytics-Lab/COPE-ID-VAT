from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data, organization_model, project_model, role_model, \
    permission_model, user_project_model, coding_variable, coding_value, inbox_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all})

@login_required
def addProject(request):
    return render(request = request,
                  template_name='main/addProject.html',
                  context = {"tutorials":Tutorial.objects.all})

@login_required
def existingProjects(request):
    user_projects = user_project_model.objects.filter(user=request.user)
    context = {
        'user_projects': user_projects,
    }
    return render(request, 'main/existingProjects.html', context)

@login_required
def existingProjects_posts(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)
    
    context = {
        'project': project,
    }
    return render(request, 'main/existingProjectsTabs/posts.html', context)

@login_required
def existingProjects_codingVariables(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)
    
    context = {
        'project': project,
    }
    return render(request, 'main/existingProjectsTabs/codingVariables.html', context)

@login_required
def existingProjects_irrFeedback(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)

    context = {
        'project': project,
    }
    return render(request, 'main/existingProjectsTabs/irrFeedback.html', context)

@login_required
def existingProjects_projectUsers(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)

    users = user_project_model.objects.filter(project=project).select_related('user')

    # Get all user_project_model instances related to the specific project
    user_projects = user_project_model.objects.filter(project=project).select_related('user', 'role')

    # Check if the user has the 'invite users' permission
    has_addedit_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='addedit-project-users').exists()
    has_download_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='codebook-all-variables-values-labels-etct').exists()
    has_delete_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='delete-the-project').exists()

    context = {
        'project': project,
        'users': users,
        'user_projects': user_projects,
        'has_addedit_permission': has_addedit_permission,
        'has_download_permission': has_download_permission,
        'has_delete_permission': has_delete_permission,
    }
    return render(request, 'main/existingProjectsTabs/projectUsers.html', context)

@login_required
def existingProjects_projectRoles(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)

    # Get all user_project_model instances related to the specific project
    user_projects = user_project_model.objects.filter(project=project).select_related('user', 'role')

    # Check if the user has the 'invite users' permission
    has_addedit_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='addedit-project-users').exists()
    has_download_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='codebook-all-variables-values-labels-etct').exists()
    has_delete_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='delete-the-project').exists()

    context = {
        'project': project,
        'user_projects': user_projects,
        'has_addedit_permission': has_addedit_permission,
        'has_download_permission': has_download_permission,
        'has_delete_permission': has_delete_permission,
    }
    return render(request, 'main/existingProjectsTabs/projectRoles.html', context)

@login_required
def users(request):
    return render(request = request,
                  template_name='main/users.html',
                  context = {"tutorials":Tutorial.objects.all})




# def register(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"New account created: {username}")
#             login(request, user)
#             return redirect("main:homepage")

#         else:
#             for msg in form.error_messages:
#                 messages.error(request, f"{msg}: {form.error_messages[msg]}")

#             return render(request = request,
#                           template_name = "main\\register.html",
#                           context={"form":form})

#     form = NewUserForm
#     return render(request = request,
#                   template_name = "main\\register.html",
#                   context={"form":form})

# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully")
#     return redirect("main:homepage")


# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('/')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request,
#                     template_name = "main/login.html",
#                     context={"form":form})

def datagrid(request):
    search_query = request.GET.get('search_query')
    if search_query:
        documents = sample_data.objects.filter(doc_text__icontains=search_query).order_by('id')
    else:
        documents = sample_data.objects.all().order_by('id')

    paginator = Paginator(documents, 25)  # Show 25 docs per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/datagrid.html', context = {"sample_data":page_obj})
    
def docInfo(request):
    page = int(request.GET.get('page'))
    doc_id = int(request.GET.get('doc_id'))
    search_query = request.GET.get('search_query', '')

    if search_query:
        docs = list(sample_data.objects.filter(Q(doc_text__icontains=search_query)).order_by('id'))
    else:
        docs = list(sample_data.objects.all().order_by('id'))

    # Get index of document being viewed
    current_index = next((index for (index, d) in enumerate(docs) if d.id == doc_id), None)

    # Return if index is not found
    if current_index is None:
        return redirect('main:datagrid')

    # Check that previous index exists
    if current_index > 0:
        previous_doc_id = docs[current_index - 1].id
    else:
        previous_doc_id = None

    # Check that next index exists
    if current_index < len(docs) - 1:
        next_doc_id = docs[current_index + 1].id
    else:
        previous_doc_id = None

    doc = docs[current_index]

    doc_info = {
        'doc_id': doc.id,
        'doc_text': doc.doc_text,
        'doc_json': doc.doc_json,
        'doc_source': doc.doc_source,
        'search_query': search_query,
        'previous_doc_id': previous_doc_id,
        'next_doc_id': next_doc_id,
        'page': page
    }

    return render(request, 'main/datagrid_modal.html', {'doc_info': doc_info})
    
def test(request):
        test = None

        return render(request, 'main/test.html', {'test': test})

