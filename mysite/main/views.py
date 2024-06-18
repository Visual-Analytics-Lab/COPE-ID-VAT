from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data, bert_main_sample_data, User, organization_model, project_model, role_model, \
    permission_model, user_project_model, coding_variable, coding_value, inbox_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, OuterRef, Subquery, Exists

# Create your views here.

# =============================================================
# Homepage
# =============================================================

def homepage(request):
    distinct_platforms = sample_data.objects.values_list('doc_source', flat=True).distinct()
    distinct_topics = bert_main_sample_data.objects.values_list('topic_name', flat=True).distinct()
    return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all,
                             "distinct_platforms": distinct_platforms,
                             "distinct_topics": distinct_topics})

# =============================================================
# Add Project
# =============================================================

@login_required
def addProject(request):
    

    return render(request = request,
                  template_name='main/addProject.html',
                  context = {"tutorials":Tutorial.objects.all})

# =============================================================
# My Projects
# =============================================================

@login_required
def myProjects(request):
    # Fetch user's projects
    user_projects = user_project_model.objects.filter(user=request.user)

    context = {
        'user_projects': user_projects,
    }
    return render(request, 'main/myProjects.html', context)

# =============================================================
# My Projects - Units
# =============================================================

@login_required
def myProjects_units(request, project_id):
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)
    
    context = {
        'project': project,
    }
    return render(request, 'main/myProjectsTabs/units.html', context)

# =============================================================
# My Projects - Codebook
# =============================================================

@login_required
def myProjects_codebook(request, project_id):
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)

    # Check user permissions
    has_edit_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='edit-codebook').exists()

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
        'has_edit_permission': has_edit_permission,
    }
    return render(request, 'main/myProjectsTabs/codebook.html', context)

# =============================================================
# My Projects - Iter-Rater Reliability
# =============================================================

@login_required
def myProjects_irr(request, project_id):
    project = get_object_or_404(project_model, project_id=project_id)

    context = {
        'project': project,
    }
    return render(request, 'main/myProjectsTabs/irr.html', context)

# =============================================================
# My Projects - Edit Project
# =============================================================

@login_required
def myProjects_editProject(request, project_id):
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)

    # Fetch project users from database
    users = user_project_model.objects.filter(project=project).select_related('user')

    roles = role_model.objects.exclude(role_name="Principal Investigator")

    # 

    # Check user permissions
    has_addedit_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='addedit-project-users').exists()
    has_edit_user_privileges = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='edit-project-users-privileges').exists()
    has_download_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='codebook-all-variables-values-labels-etc').exists()
    has_delete_permission = user_project_model.objects.filter(user=request.user, project=project, permissions__permission_slug='delete-the-project').exists()

    if request.method == 'POST':
        user_id = request.POST.get('user-id')
        print("user_id", user_id)
        project_id = project.project_id
        print("project_id", project_id)
        role_pk = request.POST.get('role-pk')
        print("role_name", role_pk)
        role = get_object_or_404(role_model, pk=role_pk)
        
        print("role:", role)

        user = get_object_or_404(User, pk=user_id)
        print("user", user)
        project = get_object_or_404(project_model, project_id=project_id)
        print("project", project)
        print("TEST0")

        user_project = get_object_or_404(user_project_model, user__pk=user_id, project__project_id=project_id)

        # Check if an instance with the same user and project exists (excluding the current instance)
        existing_user_project = user_project_model.objects.filter(user=user, project=project).exclude(pk=user_project.pk).first()

        print(user_id)
        print(project_id)
        print("TEST1")
        
        print("TEST2")
        if existing_user_project:
            print("TEST3")
            # Update the existing instance
            existing_user_project.role = role
            existing_user_project.save()
            existing_user_project.reset_permissions()
        else:
            print("TEST4")
            # Update the current instance
            user_project.user = user
            user_project.project = project
            user_project.role = role
            user_project.save()
            user_project.reset_permissions()

        print("TEST")
        return redirect('main:myProjects_editProject', project_id=project.project_id)
    
        

    context = {
        'project': project,
        'users': users,
        'roles': roles,
        'has_addedit_permission': has_addedit_permission,
        'has_edit_user_privileges': has_edit_user_privileges,
        'has_download_permission': has_download_permission,
        'has_delete_permission': has_delete_permission,
    }
    return render(request, 'main/myProjectsTabs/editProject.html', context)

# =============================================================
# My Projects - User Profile
# =============================================================

@login_required
def myProjects_userProfile(request, project_id, user_id):

    # Fetch project
    project = get_object_or_404(project_model, pk=project_id)

    # Fetch user
    user = get_object_or_404(User, pk=user_id)

    # Fetch user project instance
    user_project = user_project_model.objects.prefetch_related('permissions').get(user=user, project=project_id)

    # annotated_permissions = []
    # for perm in permissions:
    #     annotated_permission = {
    #         'permission': perm,
    #         'assigned': perm.permission_slug in user_permissions_set
    #     }
    #     annotated_permissions.append(annotated_permission)

    # Create a subquery to check if a permission is assigned to the user project
    user_project_permissions = user_project.permissions.filter(pk=OuterRef('pk'))

    # Annotate the permissions queryset with a boolean indicating if they are assigned to the user
    permissions = permission_model.objects.filter(permission_assignable=True).order_by('permission_rank').annotate(assigned=Exists(user_project_permissions))

    # Fetch roles, exclude PI
    roles = role_model.objects.exclude(role_name="Principal Investigator")

    if request.method == 'POST':

        # Get project ID from project instance
        project_id = project.project_id

        # Get user ID from HTTP POST request
        user_id = request.POST.get('user-id')

        # Get role key from HTTP POST request
        role_pk = request.POST.get('role-pk')

        # Fetch role instance from key
        role = get_object_or_404(role_model, pk=role_pk)

        user_project = get_object_or_404(user_project_model, user__pk=user_id, project__project_id=project_id)

        # Check if an instance with the same user and project exists (excluding the current instance)
        existing_user_project = user_project_model.objects.filter(user=user, project=project).exclude(pk=user_project.pk).first()
        
        if existing_user_project:
            # Update the existing instance
            existing_user_project.role = role
            existing_user_project.save()
            existing_user_project.reset_permissions()
        else:
            # Update the current instance
            user_project.user = user
            user_project.project = project
            user_project.role = role
            user_project.save()
            user_project.reset_permissions()

        return redirect('main:myProjects_userProfile', project_id=project.project_id, user_id=user_id)

    context = {
        'roles': roles,
        'user': user,
        'user_project': user_project,
        'project': project,
        'permissions': permissions,
    }
    
    return render(request, 'main/myProjectsTabs/userProfile.html', context)

# =============================================================
# My Projects - Sample & Results
# =============================================================

@login_required
def myProjects_sampleResults(request, project_id):
    # Fetch project
    project = get_object_or_404(project_model, project_id=project_id)

    context = {
        'project': project,
    }
    return render(request, 'main/myProjectsTabs/sampleResults.html', context)

# =============================================================
# Users
# =============================================================

@login_required
def users(request):
    return render(request = request,
                  template_name='main/users.html',
                  context = {"tutorials":Tutorial.objects.all})

# =============================================================
# Datagrid
# =============================================================

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
    
# =============================================================
# Doc Info
# =============================================================

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
    
# =============================================================
# Testing and Debugging
# =============================================================

def test(request):
        test = None

        return render(request, 'main/test.html', {'test': test})
