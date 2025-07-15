from django import forms
from .models import unit_assignment

class UnitAssignmentForm(forms.ModelForm):
    class Meta:
        model = unit_assignment
        fields = ["project", "unit", "coder"]

    def __init__(self, *args, **kwargs):
        project = kwargs.get("initial", {}).get("project") or kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields["unit"].queryset = project.units.all()
