from django.contrib import admin
from .models import Tutorial, sample_data, organization_model, project_model, role_model, permission_model, user_project_role_model, coding_variable, coding_value

class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
        ("Content", {"fields": ["tutorial_content"]})
    ]

class DataGridAdmin(admin.ModelAdmin):
    fieldsets = [('Document Info', {'fields': ['doc_json', 'doc_source', 'doc_text']})]

class organization_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('name', 'super_admin')

    # Set display order
    ordering = ('org_name', 'org_super_admin',)

    # Set column names & custom sorting
    def name(self, obj):
        return obj.org_name
    name.short_description = 'Organization'
    name.admin_order_field = 'org_name'

    def super_admin(self, obj):
        return obj.org_super_admin
    super_admin.short_description = 'Super Admin'
    super_admin.admin_order_field = 'org_super_admin'

class project_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'name', 'project_pi')

    # Set display order
    ordering = ('project_org', 'project_name', 'principal_investigator',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.project_org
    organization.short_description = 'Organization'

    def name(self, obj):
        return obj.project_name
    name.short_description = 'Project'

    def project_pi(self, obj):
        return obj.principal_investigator
    project_pi.short_description = 'Principal Investigator'

class role_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('acronym', 'name', 'description')

    # Set display order
    ordering = ('role_acronym', 'role_name',)

    # Set column names & custom sorting
    def name(self, obj):
        return obj.role_name
    name.short_description = 'Role'

    def acronym(self, obj):
        return obj.role_acronym
    acronym.short_description = 'Acronym'

    def description(self, obj):
        return obj.role_description
    description.short_description = 'Description'

class permission_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('name', 'description')

    # Set display order
    ordering = ('permission_name',)

    # Set column names & custom sorting
    def name(self, obj):
        return obj.permission_name
    name.short_description = 'Permission'

    def description(self, obj):
        return obj.permission_description
    description.short_description = 'Description'

class user_project_role_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'user', 'role')

    # Set display order
    ordering = ('project__project_org__org_name', 'project', 'user', 'role')

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.project.project_org.org_name
    organization.short_description = 'Organization'

    def project(self, obj):
        return obj.project
    project.short_description = 'Project'

    def user(self, obj):
        return obj.user
    user.short_description = 'User'

    def role(self, obj):
        return obj.role
    role.short_description = 'Role'

class coding_variable_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'name')

    # Set display order
    ordering = ('variable_project__project_org__org_name', 'variable_project', 'variable_name',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.variable_project.project_org.org_name
    organization.short_description = 'Organization'

    def project(self, obj):
        return obj.variable_project
    project.short_description = 'Project'

    def name(self, obj):
        return obj.variable_name
    name.short_description = 'Name'

class coding_value_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'variable', 'value')

    # Set display order
    ordering = ('variable__variable_project__project_org', 'variable__variable_project', 'variable', 'value',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.variable.variable_project.project_org
    organization.short_description = 'Organization'

    def project(self, obj):
        return obj.variable.variable_project
    project.short_description = 'Project'

    
# Register your models here.
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(sample_data, DataGridAdmin)
admin.site.register(organization_model, organization_model_admin)
admin.site.register(project_model, project_model_admin)
admin.site.register(role_model, role_model_admin)
admin.site.register(permission_model, permission_model_admin)
admin.site.register(user_project_role_model, user_project_role_model_admin)
admin.site.register(coding_variable, coding_variable_admin)
admin.site.register(coding_value, coding_value_admin)
