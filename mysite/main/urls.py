from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
  
    # Dashboard
    # =============================================================
    path("", views.dashboard, name="dashboard"),

    # Add Project (Defunct)
    # =============================================================
    path("add_project/", views.addProject, name="addProject"),

    # My Projects
    # =============================================================
    path("my_projects/", views.myProjects, name="myProjects"),
    path("my_projects/units/<uuid:project_id>/", views.myProjects_units, name="myProjects_units"),
    path("my_projects/code_unit/<uuid:project_id>/<int:unit_id>", views.myProjects_codeUnit, name="myProjects_codeUnit"),

    # My Projects - Codebook
    # =============================================================
    path("my_projects/codebook/<uuid:project_id>/", views.myProjects_codebook, name="myProjects_codebook"),
    path("my_projects/add_variable/<uuid:project_id>/", views.myProjects_addVariable, name="myProjects_addVariable"),
    path("my_projects/edit_variable/<uuid:project_id>/<int:variable_id>/", views.myProjects_editVariable, name="myProjects_editVariable"),

    # My Projects - Statistics (Will add URL for Samples & Results)
    # =============================================================
    path("my_projects/progress_irr/<uuid:project_id>/", views.myProjects_irr, name="myProjects_irr"),

    # My Projects - Edit Project
    # =============================================================
    path("my_projects/edit_project/<uuid:project_id>/", views.myProjects_editProject, name="myProjects_editProject"),
    path("my_projects/profile/<uuid:project_id>/<int:user_id>/", views.myProjects_projectProfile, name="myProjects_projectProfile"),
    path("my_projects/samples_results/<uuid:project_id>/", views.myProjects_sampleResults, name="myProjects_SampleResults"),

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
    path("my_projects/assign_test/<uuid:project_id>/", views.myProjects_assignTest, name="myProjects_assignTest"),
]