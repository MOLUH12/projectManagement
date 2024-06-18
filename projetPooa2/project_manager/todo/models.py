# todo/models.py
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, through='ProjectMember', related_name='projects')

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100, default='Coder')
    name = models.CharField(max_length=100, default='Moluh')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    resources = models.TextField(blank=True)  # Ajouter le champ resources
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    completed = models.BooleanField(default=False)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned', null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    def __str__(self):
        return f"{self.user.username} in {self.project.name}"
