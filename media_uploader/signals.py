from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, ProjectTeam

@receiver(post_save, sender=Project)
def create_project_team(sender, instance, created, **kwargs):
    if created:  # 新しく作成された場合のみ実行
        project_team = ProjectTeam.objects.create(project=instance)
        project_team.members.add(instance.owner)
