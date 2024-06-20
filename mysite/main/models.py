from django.db import models
from datetime import datetime
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import int_list_validator


# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.tutorial_title
    
class sample_data(models.Model):
    id = models.IntegerField
    doc_text = models.TextField()
    doc_json = models.TextField()
    doc_source = models.CharField(max_length=150)

    def __str__(self):
        return self.doc_json
      
class bert_main_sample_data(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.TextField()
    documents = models.CharField()

    def __str__(self):
        return self.doc_json
    
    class Meta:
        db_table = 'main_bert_main_sample_data'

class organization_model(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    org_super_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='organization_super_admin')
    org_users = models.ManyToManyField(User, related_name='organization_users')

    def __str__(self):
        return self.org_name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

class project_model(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=128, null=False, blank=False)
    project_org = models.ForeignKey(organization_model, on_delete=models.CASCADE, default='')
    principal_investigator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    N = models.PositiveIntegerField(default=0) # Total number of unique units

    def __str__(self):
        return self.project_name
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class role_model(models.Model):
    role_name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    role_acronym = models.CharField(max_length=8, unique=True, null=False, blank=False)
    role_description = models.TextField(max_length=128, blank=True, default='')
    role_permissions = models.ManyToManyField('permission_model', related_name='roles', blank=True)

    def __str__(self):
        return self.role_name
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

class permission_model(models.Model):
    permission_name = models.CharField(max_length=64, unique=False, null=False, blank=False)
    permission_slug = models.SlugField(max_length=64, unique=False, blank=True, editable=True)
    permission_description = models.TextField(max_length=128, default='', null=True, blank=True)

    PERM_CATEGORY = (
    ('select', 'Select a Category'),
    ('profile', 'Project Profile Privileges'),
    ('codebook', 'Codebook Privileges'),
    ('analysis', 'Units of Analysis & Coding Privileges'),
    ('irr', 'Inter-Rater Reliability Privileges'),
    ('results', 'Sample & Results Privileges'),
    ('export', 'Download & Export Privileges'),
    )

    permission_category = models.CharField(
        max_length=16,
        choices=PERM_CATEGORY,
        blank=False,
        default='select',
        help_text='Permission Category',
    )

    def __str__(self):
        return self.permission_name
    
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    # Handle creation and updating of slugified name
    # Slug used to check permissions
    def save(self, *args, **kwargs):
        self.permission_slug = slugify(self.permission_name)
        super(permission_model, self).save(*args, **kwargs)

class user_project_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    project = models.ForeignKey(project_model, on_delete=models.CASCADE, blank=False)
    role = models.ForeignKey(role_model, on_delete=models.CASCADE, blank=False)
    permissions = models.ManyToManyField(permission_model, blank=True)
    n = models.PositiveIntegerField(default=0) # Total number of units assigned

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = "User Project Role"
        verbose_name_plural = "Users Projects Roles"

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name} - {self.role.role_name}"
    
    def reset_permissions(self):
        print("1 self.permissions:", list(self.permissions.all()))
        self.permissions.clear()
        self.permissions.add(*self.role.role_permissions.all())
        print("2 self.permissions:", list(self.permissions.all()))

@receiver(post_save, sender=user_project_model)
def reset_permissions_post_save(sender, instance, **kwargs):
    instance.reset_permissions()

class coding_variable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    variable_name = models.CharField(max_length=128, null=False, blank=False)
    variable_description = models.TextField(max_length=128, default='')
    variable_project = models.ForeignKey(project_model, on_delete=models.CASCADE)

    def __str__(self):
        return self.variable_name

    class Meta:
        verbose_name = "Coding Variable"
        verbose_name_plural = "Coding Variables"

    # Get a list of variable values
    def get_values(self):
        values = self.values.all()
        return ", ".join([f"{value.value}" for value in values])
    
class coding_value(models.Model):
    variable = models.ForeignKey(coding_variable, on_delete=models.CASCADE, related_name='values')
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=8, null=False, blank=False)
    other = models.CharField(max_length=128, null=True, blank=True)
    other_bool = models.BooleanField(default=False)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = "Coding Value"
        verbose_name_plural = "Coding Values"

class inbox_model(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    message = models.TextField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} for {self.project.project_name}"

    class Meta:
        verbose_name = "Inbox"
        verbose_name_plural = "Inbox"
    
