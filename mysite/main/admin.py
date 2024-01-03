from django.contrib import admin
from .models import Tutorial, sample_data

class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
        ("Content", {"fields": ["tutorial_content"]})
    ]

class DataGridAdmin(admin.ModelAdmin):
    fieldsets = [('Document Info', {'fields': ['doc_json', 'doc_source', 'doc_text']})]
# Register your models here.
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(sample_data, DataGridAdmin)