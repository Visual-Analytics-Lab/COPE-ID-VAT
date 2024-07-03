from django.contrib.auth.models import User

def sys_admin_test(user):
    if user.is_authenticated:
        return user.groups.filter(name='System Admin').exists()
    return False

def authorized_user_test(user):
    return user.group.filter(name='Authorized Tool User').exists()