from django.contrib import admin
from .models import Tutorial, sample_data, organization_model, project_model, role_model, permission_model, user_project_model, coding_variable, coding_value, inbox_model

# =============================================================
# Tutorial Admin
# =============================================================

class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
        ("Content", {"fields": ["tutorial_content"]})
    ]

# =============================================================
# Data Grid Admin
# =============================================================

class DataGridAdmin(admin.ModelAdmin):
    fieldsets = [('Document Info', {'fields': ['doc_json', 'doc_source', 'doc_text']})]

# =============================================================
# Organization Model Admin
# =============================================================

class organization_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('name', 'super_admin')

    # Set filter options
    list_filter = ('org_name',)

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

# =============================================================
# Project Model Admin
# =============================================================

class project_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'name', 'project_pi')

    # Set filter options
    list_filter = ('project_org', 'project_name',)

    # Set display order
    ordering = ('project_org', 'project_name', 'principal_investigator',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.project_org
    organization.short_description = 'Organization'
    organization.admin_order_field = 'project_org'  

    def name(self, obj):
        return obj.project_name
    name.short_description = 'Project'
    name.admin_order_field = 'project_name'

    def project_pi(self, obj):
        return obj.principal_investigator
    project_pi.short_description = 'Principal Investigator'
    project_pi.admin_order_field = 'principal_investigator'

# =============================================================
# Role Model Admin
# =============================================================

class role_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('acronym', 'name', 'description')

    # Set display order
    ordering = ('role_acronym', 'role_name',)

    # Set column names & custom sorting
    def acronym(self, obj):
        return obj.role_acronym
    acronym.short_description = 'Acronym'
    acronym.admin_order_field = 'role_acronym'

    def name(self, obj):
        return obj.role_name
    name.short_description = 'Role'
    name.admin_order_field = 'role_name'

    def description(self, obj):
        return obj.role_description
    description.short_description = 'Description'

# =============================================================
# Permission Model Admin
# =============================================================

class permission_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('permission_rank', 'name', 'category', 'description', 'permission_assignable')

    # Set display order
    ordering = ('permission_rank', 'permission_category', 'permission_name', 'permission_assignable',)

    # Set column names & custom sorting
    def name(self, obj):
        return obj.permission_name
    name.short_description = 'Permission'
    name.admin_order_field = 'permission_name'

    def category(self, obj):
        return obj.get_permission_category_display()
    category.short_description = 'Category'
    category.admin_order_field = 'permission_category'

    def description(self, obj):
        return obj.permission_description
    description.short_description = 'Description'

# =============================================================
# User Project Model Admin
# =============================================================

class user_project_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'user', 'role')

    # Set filter options
    list_filter = ('project__project_org__org_name', 'project',)

    # Set display order
    ordering = ('project__project_org__org_name', 'project', 'user', 'role')

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.project.project_org.org_name
    organization.short_description = 'Organization'
    organization.admin_order_field = 'project__project_org__org_name'

    def project(self, obj):
        return obj.project
    project.short_description = 'Project'

    def user(self, obj):
        return obj.user
    user.short_description = 'User'

    def role(self, obj):
        return obj.role
    role.short_description = 'Role'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.reset_permissions()

# =============================================================
# Coding Variable Admin
# =============================================================

class coding_variable_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'name')

    # Set filter options
    list_filter = ('variable_project__project_org__org_name', 'variable_project',)

    # Set display order
    ordering = ('variable_project__project_org__org_name', 'variable_project', 'variable_name',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.variable_project.project_org.org_name
    organization.short_description = 'Organization'
    organization.admin_order_field = 'variable_project__project_org__org_name'

    def project(self, obj):
        return obj.variable_project
    project.short_description = 'Project'
    project.admin_order_field = 'variable_project'

    def name(self, obj):
        return obj.variable_name
    name.short_description = 'Name'
    name.admin_order_field = 'variable_name'

# =============================================================
# Coding Value Admin
# =============================================================

class coding_value_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'variable', 'value')

    # Set filter options
    list_filter = ('variable__variable_project__project_org', 'variable__variable_project', 'variable')

    # Set display order
    ordering = ('variable__variable_project__project_org', 'variable__variable_project', 'variable', 'value',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.variable.variable_project.project_org
    organization.short_description = 'Organization'
    organization.admin_order_field = 'variable__variable_project__project_org'

    def project(self, obj):
        return obj.variable.variable_project
    project.short_description = 'Project'
    project.admin_order_field = 'variable__variable_project'

# =============================================================
# Inbox Model Admin
# =============================================================

class inbox_model_admin(admin.ModelAdmin):
    # Set display columns
    list_display = ('organization', 'project', 'timestamp', 'sender', 'recipient')

    # Set filter options
    list_filter = ('project__project_org', 'project', 'timestamp', 'sender', 'recipient',)

    # Set display order
    ordering = ('project__project_org', 'project', 'timestamp', 'sender', 'recipient',)

    # Set column names & custom sorting
    def organization(self, obj):
        return obj.project.project_org
    organization.short_description = 'Organization'
    organization.admin_order_field = 'project__project_org'

    def project(self, obj):
        return obj.project
    project.short_description = 'Project'
    project.admin_order_field = 'variable__variable_project'



# =============================================================
# Admin Page Registration
# =============================================================

admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(sample_data, DataGridAdmin)
admin.site.register(organization_model, organization_model_admin)
admin.site.register(project_model, project_model_admin)
admin.site.register(role_model, role_model_admin)
admin.site.register(permission_model, permission_model_admin)
admin.site.register(user_project_model, user_project_model_admin)
admin.site.register(coding_variable, coding_variable_admin)
admin.site.register(coding_value, coding_value_admin)
admin.site.register(inbox_model, inbox_model_admin)