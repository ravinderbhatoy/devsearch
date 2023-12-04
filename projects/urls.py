from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.single_project, name='single-project'),
    path('create-project/', views.create_project, name='create-project'),
    path('update-project/<str:pk>/', views.update_project, name='update-project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),

    path('remove-tag/<str:project_id>/<str:tag_id>/', views.remove_tag, name='remove-tag'),
]

