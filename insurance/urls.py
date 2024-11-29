from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('insuarnce/signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('policy/<str:policy_name>/', views.policy_details, name='policies_details'),
    path('profile/', views.user_profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('upgrade_policy/<str:policy_name>/', views.upgrade_policy, name='upgrade_policy'),
    path('buy_policy/<str:policy_name>/', views.buy_policy, name='buy_policy'),
    path('update_policy/<str:policy_name>/', views.update_policy, name='update_policy'),
    path('delete_policy/<str:policy_name>/', views.delete_policy, name='delete_policy'),
    path('add_policy/', views.add_policy, name='add_policy'),
    path('view_all_users/', views.view_all_users, name='view_all_users'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
    path('delete_policy_admin/<str:policy_name>/', views.delete_policy_admin, name='delete_policy_admin'),
]