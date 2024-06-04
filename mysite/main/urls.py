from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("add_project/", views.addProject, name="addProject"),
    path("existing_project/", views.existingProjects, name="existingProjects"),
    path("users/", views.users, name="users"),
    path("existing_project/posts/", views.existingProjects_posts, name="existingProjects_posts"),
    path("existing_project/coding_variables/", views.existingProjects_codingVariables, name="existingProjects_coding_variables"),
    path("existing_project/irr_feedback/", views.existingProjects_irrFeedback, name="existingProjects_irrFeedback"),
    path("existing_project/project_users/", views.existingProjects_projectUsers, name="existingProjects_projectUsers"),
    path("existing_project/project_roles/", views.existingProjects_projectRoles, name="existingProjects_projectRoles"),
    # path("register/", views.register, name="register"),
    # path("logout", views.logout_request, name="logout"),
    # path("login", views.login_request, name="login"),
    path("datagrid/", views.datagrid, name="datagrid"),
    path('doc_info/', views.docInfo, name='docInfo'),
    path('test/', views.test, name='test'),
]