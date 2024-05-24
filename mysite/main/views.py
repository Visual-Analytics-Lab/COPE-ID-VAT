from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, sample_data
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
import platform

# Create your views here.
def homepage(request):
    if platform.platform().startswith('Windows'):
        return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all})
    else:
        return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all})

def addproject(request):
    return render(request = request,
                  template_name='main/addproject.html',
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

    paginator = Paginator(documents, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/datagrid.html', context = {"sample_data":page_obj})
    
def doc_info(request):
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

