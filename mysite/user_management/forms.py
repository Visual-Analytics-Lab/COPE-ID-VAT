from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import my_profile_model


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = my_profile_model
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(label='Group Name', max_length=100)
    users = forms.ModelMultipleChoiceField(queryset=my_profile_model.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    
class AdminAddUser(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailInput()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

class AccountUpdateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    department = forms.CharField(required=False)
    organization = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = my_profile_model
        fields = ['first_name', 'last_name', 'email', 'title', 'department', 'organization', 'city', 'state', 'zip_code', 'country']

class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None