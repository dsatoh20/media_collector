from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_unique_filename(instance, filename):
    # ユニークな名前をつける
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return f"images/{instance.project.title}/{unique_filename}"

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_owner')
    title = models.CharField(max_length=20)
    pub = models.BooleanField(default=0)
    labels = models.JSONField(default=[])
    start_date = models.DateTimeField(auto_now_add=True)
    
    def  __str__(self):
        return '<' + self.title + '(created by ' + self.owner.username + ')'+ '>'
    
class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_owner')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_unique_filename)
    label = models.IntegerField(default=-1)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '<' + self.project.title + '(uploaded by ' + self.owner.username + ')'+ '>'
    
class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='member')
    
    def __str__(self):
        return '<Team of ' + self.project.title + '>'
    
    
