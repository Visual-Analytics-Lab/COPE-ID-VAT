from django.urls import path
from . import views


app_name = 'user_management'  # here for namespacing of urls.

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("manage_users/", views.manage_users, name="manage_users"),
    path('create_group/', views.create_group, name='create_group'),
    path('account/', views.account, name='account'),
    path('account/update/', views.account_update, name='account_update'),
]