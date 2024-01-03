from django.db import models
from datetime import datetime

# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.tutorial_title
    
class sample_data(models.Model):
    doc_text = models.TextField()
    doc_json = models.TextField()
    doc_source = models.CharField(max_length=150)
