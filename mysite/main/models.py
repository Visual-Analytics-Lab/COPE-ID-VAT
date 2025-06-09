from django.db import models
from datetime import datetime
import uuid
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import int_list_validator, MinValueValidator, MaxValueValidator
from django.conf import settings
import json

User = settings.AUTH_USER_MODEL

# Create your models here.

# =============================================================
# Tutorial
# =============================================================

class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.tutorial_title
    
# =============================================================
# Sample Data
# =============================================================

class sample_data(models.Model):
    id = models.IntegerField
    doc_text = models.TextField(null=True)
    doc_json = models.TextField(null=True)
    doc_source = models.CharField(max_length=150)

    def __str__(self):
        return self.doc_json

    # tweetLanguage, tweetMentions, tweetHashtags, tweetAnnotations, tweetURLs, retweetCount, replyCount, likeCunt, and createdAt

    @property
    def created_at(self):
        try:
            doc_json_data = json.loads(self.doc_json)
            # Try to get 'createdAt' first, then fall back to 'created_at'
            return doc_json_data.get("createdAt") or doc_json_data.get("created_at", "N/A")
        except json.JSONDecodeError:
            return "Invalid JSON"
    
# =============================================================
# Bert Main Sample Data
# =============================================================

class bert_main_sample_data(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.TextField()
    documents = models.CharField()
 
    def __str__(self):
        return self.topic_name
   
    class Meta:
        db_table = 'main_bert_main_sample_data'

# =============================================================
# Organization Model
# =============================================================

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

# =============================================================
# Project Model
# =============================================================

class project_model(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=128, null=False, blank=False)
    project_org = models.ForeignKey(organization_model, on_delete=models.CASCADE, default='')
    principal_investigator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    N = models.PositiveIntegerField(default=0) # Total number of unique units
    cluster = models.BooleanField(default=False)
    platform_units = JSONField(default=dict, blank=True)
    SAMPLE_PREFERENCE = (
    ('simple', 'Simple Random Sample'),
    ('systematic', 'Systematic Random Sampling'),
    ('chronologically', 'Chronologically by unit post ID'),
    )

    sample_preference = models.CharField(
        max_length=16,
        choices=SAMPLE_PREFERENCE,
        blank=False,
        default='chronologically',
        help_text='Sample Preference',
    )
    project_description = models.TextField(null=True, blank=True)
    codebook_protocol = models.TextField(null=True, blank=True)
    units = models.ManyToManyField(sample_data, related_name='projects', blank=True)

    def __str__(self):
        return self.project_name
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

# =============================================================
# Project List Model
# =============================================================

class project_list_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = "Favorite Project"
        verbose_name_plural = "Favorite Projects"

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name}"

# =============================================================
# Role Model
# =============================================================

class role_model(models.Model):
    role_name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    role_acronym = models.CharField(max_length=8, unique=True, null=False, blank=False)
    role_description = models.TextField(max_length=1024, blank=True, default='')
    role_permissions = models.ManyToManyField('permission_model', related_name='roles', blank=True)

    def __str__(self):
        return self.role_name
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

# =============================================================
# Permission Model
# =============================================================

class permission_model(models.Model):
    permission_name = models.CharField(max_length=64, unique=False, null=False, blank=False)
    permission_slug = models.SlugField(max_length=64, unique=False, blank=True, editable=False)
    permission_description = models.TextField(max_length=256, default='', null=True, blank=True)
    permission_rank = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)
    permission_assignable = models.BooleanField(default=False)

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

# =============================================================
# User Project Model
# =============================================================

class user_project_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    project = models.ForeignKey(project_model, on_delete=models.CASCADE, blank=False)
    role = models.ForeignKey(role_model, on_delete=models.CASCADE, blank=False)
    permissions = models.ManyToManyField(permission_model, blank=True, related_name='permissions')
    n = models.PositiveIntegerField(default=0) # Total number of units assigned
    favorite = models.BooleanField(default=False)

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
    if instance._state.adding:
        return  # Skip the signal for newly created instances
    else:
        previous_instance = user_project_model.objects.get(pk=instance.pk)
        if previous_instance.role != instance.role:
            instance.reset_permissions()
        elif set(previous_instance.permissions.all()) != set(instance.permissions.all()):
            instance.reset_permissions()

# =============================================================
# Coding Variable - (Note: Save codebook for reuse)
# =============================================================

class coding_variable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    variable_name = models.CharField(max_length=64, null=False, blank=False)
    variable_description = models.TextField(max_length=1024, default='')
    variable_project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    variable_rank = models.SmallIntegerField(unique=True, validators=[MinValueValidator(-100), MaxValueValidator(100)])

    MEASUREMENTS = (
    ('nom', 'Nominal'),
    ('ord', 'Ordinal'),
    ('int', 'Interval'),
    ('rate', 'Ratio'),
    ('none', 'None'),
    )

    variable_measurement = models.CharField(
        max_length=8,
        choices=MEASUREMENTS,
        blank=False,
        default='nom',
        help_text='Level of Measurement',
    )

    def __str__(self):
        return self.variable_name

    class Meta:
        verbose_name = "Coding Variable"
        verbose_name_plural = "Coding Variables"
        indexes = [
            models.Index(fields=['variable_project']),
        ]
    
    # Get a list of variable values
    def get_values(self):
        return self.values.all()
    
    # Get a list of comma-separated variable values
    def get_values_comma(self):
        values = self.values.all()
        return ", ".join([f"{value.value}" for value in values])
    
    # Get list of measurement types
    @classmethod
    def get_measurements_list(cls):
        return [name for _, name in cls.MEASUREMENTS]

# =============================================================
# Coding Value
# =============================================================

class coding_value(models.Model):
    variable = models.ForeignKey(coding_variable, on_delete=models.CASCADE, related_name='values')
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=8, null=False, blank=False)
    example = models.TextField(null=True, blank=True)
    example_bool = models.BooleanField(default=False)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = "Coding Value"
        verbose_name_plural = "Coding Values"
        indexes = [
            models.Index(fields=['variable']),
        ]

# =============================================================
# Post Coding
# =============================================================

class unit_coding(models.Model):
    unit = models.ForeignKey(sample_data, on_delete=models.CASCADE)
    variable = models.ForeignKey(coding_variable, on_delete=models.CASCADE)
    value = models.ForeignKey(coding_value, on_delete=models.CASCADE)
    project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this to track who did the coding

    class Meta:
        unique_together = ('unit', 'variable', 'project', 'user')  # Ensure uniqueness per unit, variable, project, and user

    def __str__(self):
        return f"{self.unit} - {self.variable} - {self.value} (Project: {self.project}, User: {self.user})"
    
    def output(self):
        return {
            'variable_name': self.variable.variable_name,
            'variable_values': [
                {
                    'value': value.value,
                    'selected': value == self.value  # True if this value is selected, False otherwise
                } for value in self.variable.get_values()
            ],
            'value': self.value.value  # This can be used to show the selected value
        }
    
# =============================================================
# Inbox Model
# =============================================================

class inbox_model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    project = models.ForeignKey(project_model, on_delete=models.CASCADE)
    message = models.TextField(max_length=512, blank=True)
    role = models.ForeignKey(role_model, on_delete=models.CASCADE, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} for {self.project.project_name}"

    class Meta:
        verbose_name = "Inbox"
        verbose_name_plural = "Inbox"
    

# =============================================================
# Test Model
# =============================================================

class test_model(models.Model):
    content = models.TextField() 

    def __str__(self):
        return f"{self.content}"
