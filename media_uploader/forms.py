from django import forms
from .models import Project, File, ProjectTeam
from django.contrib.auth.models import User


# Projectを作成する
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'pub', 'labels']
        
    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type here...',
                'row': 1,
                "required": True
                },
        )
        self.fields['pub'].widget = forms.CheckboxInput(
            attrs={
                "required": False,
            }
        )
        self.fields['pub'].initial = False
        self.fields['labels'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type like ["dog", "cat"]',
                'row': 1,
                "required": True
            }
        )
        
# Projectを選択する
class ProjectSelectForm(forms.Form):
    project = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    def __init__(self, *args, **kwargs):
        super(ProjectSelectForm, self).__init__(*args, **kwargs)
        # publicプロジェクト or 所属チームのプロジェクトでfilterしたい(未実装：下記ではすべて取得)
        self.fields['project'].choices = [(project.id, project.title) for project in Project.objects.all()]

# Fileをアップロードする
class FileUploadeForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['image', 'label']
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(FileUploadeForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                "required": True,
                }
            )
        # Label field の選択肢を動的に設定
        self.fields['label'] = forms.ChoiceField(
            choices=[],
            widget=forms.Select(
                attrs={
                    'class': 'form-select',
                    "required": True,
                    }
                ),
            
        )
        if project:
            # labelはvalueで取得されるので、indexに直す
            labels = project.labels
            self.fields['label'].choices = [(-1, 'unknown')] + [(id, labels[id]) for id in range(len(labels))]