from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("add_project/", views.addProject, name="addProject"),
    path("my_projects/", views.myProjects, name="myProjects"),
    path("users/", views.users, name="users"),
    path("my_projects/units/<uuid:project_id>/", views.myProjects_units, name="myProjects_units"),
    path("my_projects/codebook/<uuid:project_id>/", views.myProjects_codebook, name="myProjects_codebook"),
    path("my_projects/irr/<uuid:project_id>/", views.myProjects_irr, name="myProjects_irr"),
    path("my_projects/edit_project/<uuid:project_id>/", views.myProjects_editProject, name="myProjects_editProject"),
    path("my_projects/project_roles/<uuid:project_id>/", views.myProjects_projectRoles, name="myProjects_projectRoles"),
    # path("register/", views.register, name="register"),
    # path("logout", views.logout_request, name="logout"),
    # path("login", views.login_request, name="login"),
    path("datagrid/", views.datagrid, name="datagrid"),
    path('doc_info/', views.docInfo, name='docInfo'),
    path('test/', views.test, name='test'),
]