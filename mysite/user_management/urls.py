from django.urls import path
from . import views


app_name = 'user_management'  # here for namespacing of urls.

urlpatterns = [
    # Authentication
    # =============================================================
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),

    # Manage
    # =============================================================
    path("manage_users/", views.manage_users, name="manage_users"),
    path('create_group/', views.create_group, name='create_group'),

    # Account
    # =============================================================
    path('account/', views.account, name='account'),
    path('account/update/', views.account_update, name='account_update'),

    # Users (Admin only)
    # =============================================================
    path('users/', views.UsersListView.as_view(), name='users'),
    path('update_user_groups/<int:user_id>/', views.UserGroupUpdateView.as_view(), name='update_user_groups'),
]