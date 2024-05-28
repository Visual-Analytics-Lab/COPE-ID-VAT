from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("add_project/", views.addProject, name="addProject"),
    path("existing_project/", views.existingProjects, name="existingProjects"),
    # path("register/", views.register, name="register"),
    # path("logout", views.logout_request, name="logout"),
    # path("login", views.login_request, name="login"),
    path("datagrid/", views.datagrid, name="datagrid"),
    path('doc_info/', views.docInfo, name='docInfo'),
    path('test/', views.test, name='test'),
]