from django.db import models
from datetime import datetime
import uuid
from django.contrib.auth.models import User

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

class organization_model(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_name = models.CharField(max_length=128)
    org_users = models.ManyToManyField(User)

    def __str__(self):
        return self.org_name

class project_model(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=128)
    project_org = models.ForeignKey(organization_model, on_delete=models.CASCADE, default='')
    principal_investigator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.project_name

class role_model(models.Model):
    role_name = models.CharField(max_length=64)
    role_permissions = models.ManyToManyField('permission_model', related_name='roles')

    def __str__(self):
        return self.role_name

class permission_model(models.Model):
    permission_name = models.CharField(max_length=64)

    def __str__(self):
        return self.permission_name

class user_project_role_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    role = models.ForeignKey(role_model, on_delete=models.CASCADE)
    custom_permissions = models.ManyToManyField(permission_model, blank=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name} - {self.role.role_name}"

class coding_variable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    variable_name = models.CharField(max_length=128)
    variable_description = models.TextField()
    project_id = models.ForeignKey(project_model, on_delete=models.CASCADE)

    def __str__(self):
        return self.variable_name
    
class coding_value(models.Model):
    variable = models.ForeignKey(coding_variable, on_delete=models.CASCADE)
    value = models.CharField(max_length=8)
    label = models.CharField(max_length=128)

    def __str__(self):
        return self.value
    
    
# ▒▒▒▒▒▒▒▒▒▄▄▄▄▒▒▒▒▒▒▒
# ▒▒▒▒▒▒▄▀▀▓▓▓▀█▒▒▒▒▒▒
# ▒▒▒▒▄▀▓▓▄██████▄▒▒▒▒
# ▒▒▒▄█▄█▀░░▄░▄░█▀▒▒▒▒
# ▒▒▄▀░██▄░░▀░▀░▀▄▒▒▒▒
# ▒▒▀▄░░▀░▄█▄▄░░▄█▄▒▒▒
# ▒▒▒▒▀█▄▄░░▀▀▀█▀▒▒▒▒▒
# ▒▒▒▄▀▓▓▓▀██▀▀█▄▀▀▄▒▒
# ▒▒█▓▓▄▀▀▀▄█▄▓▓▀█░█▒▒
# ▒▒▀▄█░░░░░█▀▀▄▄▀█▒▒▒
# ▒▒▒▄▀▀▄▄▄██▄▄█▀▓▓█▒▒
# ▒▒█▀▓█████████▓▓▓█▒▒
# ▒▒█▓▓██▀▀▀▒▒▒▀▄▄█▀▒▒
# ▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒