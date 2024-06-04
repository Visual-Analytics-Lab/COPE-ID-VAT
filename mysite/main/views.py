from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data, bert_main_sample_data
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

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

    paginator = Paginator(documents, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/datagrid.html', context = {"sample_data":page_obj})
    
def docInfo(request):
    if request.method == 'POST':
        # Get the doc ID from the form submission
        doc_id = request.POST.get('doc_id')
        # Retrieve the person object from the database
        doc = get_object_or_404(sample_data, pk=doc_id)
        # Prepare person data to be sent back as JSON response
        doc_info = {
            'doc_id': doc.id,
            'doc_text': doc.doc_text,
            'doc_json': doc.doc_json,
            'doc_source': doc.doc_source
        }
        # Return JSON response with person data
        return render(request, 'main/datagrid_modal.html', {'doc_info': doc_info})
    
def test(request):
        test = None

        return render(request, 'main/test.html', {'test': test})
