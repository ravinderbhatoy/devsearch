from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.profiles, name='profiles' ),
    path('user-profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('account/', views.user_account, name='account'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),

    path('create-skill/', views.create_skill, name='create-skill'),
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),

    path('inbox/', views.all_messages, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('add_message/<str:pk>/', views.add_message, name='add-message'),
]