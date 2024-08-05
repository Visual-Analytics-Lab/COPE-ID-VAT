from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import my_profile_model

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = my_profile_model

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = my_profile_model

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    model = my_profile_model

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('title', 'department', 'organization', 'city', 'state', 'zip_code', 'country')}),
    )

admin.site.register(my_profile_model, MyUserAdmin)