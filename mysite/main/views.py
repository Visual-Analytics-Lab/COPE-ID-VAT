from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data, bert_main_sample_data, organization_model, project_model, role_model, \
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
    distinct_platforms = sample_data.objects.values_list('doc_source', flat=True).distinct()
    distinct_topics = bert_main_sample_data.objects.values_list('topic_name', flat=True).distinct()
    return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all,
                             "distinct_platforms": distinct_platforms,
                             "distinct_topics": distinct_topics})

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
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)

    # Fetch project variables from database
    coding_variables = coding_variable.objects.filter(variable_project=project).prefetch_related('values')

    # Check if form was submitted
    if request.method == 'POST':

        # Check if variable id is in form
        if 'variable-id' in request.POST:

            # Get variable id
            id = request.POST.get('variable-id')
            
            # Get project id
            project_id = request.POST.get('project-id')

            # Fetch variable from database
            variable = get_object_or_404(coding_variable, pk=id, variable_project=project_id)

            # Delete the variable
            variable.delete()

        else:
            # Get variable name
            variable_name = request.POST.get('variable-name')

            # Get variable description
            variable_description = request.POST.get('variable-description')

            # Get variable values
            values = request.POST.getlist('value[]')

            # Get variable labels
            labels = request.POST.getlist('label[]')

            # Create variable
            new_variable = coding_variable(
                variable_name=variable_name,
                variable_description=variable_description,
                variable_project=project
            )
            new_variable.save()

            # Create values and labels
            for value, label in zip(values, labels):
                new_value = coding_value(
                    variable=new_variable,
                    value=value,
                    label=label
                )
                new_value.save()

        # Redirect/refresh page after form submission
        return redirect(request.path_info)

    context = {
        'project': project,
        'coding_variables': coding_variables,
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
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)

    # Fetch project users from database
    users = user_project_model.objects.filter(project=project).select_related('user') # I need to remove this line at some point and use user_projects instead

    # Fetch project users and their roles from database
    user_projects = user_project_model.objects.filter(project=project).select_related('user', 'role')

    # Check user permissions
    has_addedit_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='addedit-project-users').exists()
    has_edit_user_privileges = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='edit-project-users-privileges').exists()
    has_download_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='codebook-all-variables-values-labels-etc').exists()
    has_delete_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='delete-the-project').exists()

    context = {
        'project': project,
        'users': users,
        'user_projects': user_projects,
        'has_addedit_permission': has_addedit_permission,
        'has_edit_user_privileges': has_edit_user_privileges,
        'has_download_permission': has_download_permission,
        'has_delete_permission': has_delete_permission,
    }
    return render(request, 'main/existingProjectsTabs/projectUsers.html', context)

@login_required
def existingProjects_projectRoles(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)

    # Fetch project users and their roles from database
    user_projects = user_project_model.objects.filter(project=project).select_related('user', 'role')

    # Check user permissions
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
