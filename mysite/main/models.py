from django.db import models
from datetime import datetime
from django.core.validators import int_list_validator
import uuid

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
    topic_id = models.IntegerField()
    topic_name = models.TextField()
    documents = models.CharField()

    def __str__(self):
        return self.doc_json
    
    class Meta:
        db_table = 'main_bert_main_sample_data'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_group_id = models.IntegerField
    project_name = models.CharField(max_length=150)
    project_coding_variables = models.JSONField
    project_users = models.JSONField

    def __str__(self):
        return self.project_name

class CodingVariable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    variable_name = models.CharField(max_length=150)
    variable_description = models.TextField
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.variable_name
    
class CodingValue(models.Model):
    variable = models.ForeignKey(CodingVariable, on_delete=models.CASCADE)
    value = models.CharField(max_length=150)

    def __str__(self):
        return self.value