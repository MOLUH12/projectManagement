# todo/urls.py
from django.urls import path
from . import views


# todo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('create_project/', views.create_project, name='create_project'),
    path('create_task/<int:project_id>/', views.create_task, name='create_task'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    
]