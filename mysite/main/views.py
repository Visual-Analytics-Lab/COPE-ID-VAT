from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data, bert_main_sample_data
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
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

def addProject(request):
    

    return render(request = request,
                  template_name='main/addProject.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects(request):
    return render(request = request,
                  template_name='main/existingProjects.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects_posts(request):
    return render(request = request,
                  template_name='main/existingProjectsTabs/posts.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects_codingVariables(request):
    return render(request = request,
                  template_name='main/existingProjectsTabs/codingVariables.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects_irrFeedback(request):
    return render(request = request,
                  template_name='main/existingProjectsTabs/irrFeedback.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects_projectUsers(request):
    return render(request = request,
                  template_name='main/existingProjectsTabs/projectUsers.html',
                  context = {"tutorials":Tutorial.objects.all})

def existingProjects_projectRoles(request):
    return render(request = request,
                  template_name='main/existingProjectsTabs/projectRoles.html',
                  context = {"tutorials":Tutorial.objects.all})

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
