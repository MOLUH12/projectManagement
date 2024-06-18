# todo/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, ProjectMember
from .forms import ProjectForm, TaskForm
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from django.views.decorators.csrf import csrf_protect

@csrf_protect

@login_required
def dashboard(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'todo/dashboard.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.tasks.all()
    return render(request, 'todo/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            ProjectMember.objects.create(project=project, user=request.user)
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'todo/create_project.html', {'form': form})

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'todo/create_task.html', {'form': form, 'project': project})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'todo/register.html', {'form': form})



@require_POST
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        status = request.POST.get('status')
        task.status = status
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})