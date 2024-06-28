from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
  
    # Dashboard
    # =============================================================
    path("", views.homepage, name="homepage"),

    # Add Project (Defunct)
    # =============================================================
    path("add_project/", views.addProject, name="addProject"),

    # My Projects
    # =============================================================
    path("my_projects/", views.myProjects, name="myProjects"),
    path("my_projects/units/<uuid:project_id>/", views.myProjects_units, name="myProjects_units"),

    # My Projects - Codebook
    # =============================================================
    path("my_projects/codebook/<uuid:project_id>/", views.myProjects_codebook, name="myProjects_codebook"),
    path("my_projects/add_variable/<uuid:project_id>/", views.myProjects_addVariable, name="myProjects_addVariable"),
    path("my_projects/edit_variable/<uuid:project_id>/<int:variable_id>/", views.myProjects_editVariable, name="myProjects_editVariable"),

    # My Projects - Statistics (Will add URL for Samples & Results)
    # =============================================================
    path("my_projects/irr/<uuid:project_id>/", views.myProjects_irr, name="myProjects_irr"),

    # My Projects - Edit Project (Move profile later)
    # =============================================================
    path("my_projects/edit_project/<uuid:project_id>/", views.myProjects_editProject, name="myProjects_editProject"),
    path("my_projects/profile/<uuid:project_id>/<int:user_id>/", views.myProjects_userProfile, name="myProjects_userProfile"),
    path("my_projects/project_roles/<uuid:project_id>/", views.myProjects_sampleResults, name="myProjects_SampleResults"),

    # Users (Admin only) (Move later)
    # =============================================================
    path("users/", views.users, name="users"),

    # Inbox
    # =============================================================
    path('inbox/', views.inbox, name='inbox'),

    # Datagrid
    # =============================================================
    path("datagrid/", views.datagrid, name="datagrid"),
    path('doc_info/', views.docInfo, name='docInfo'),

    # Testing
    # =============================================================
    path('test/', views.test, name='test'),
]