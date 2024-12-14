from django.shortcuts import render, redirect
from .forms import CreateProjectForm, ProjectSelectForm, FileUploadeForm
from .models import Project, File, ProjectTeam
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
import zipfile
from io import BytesIO

# project一覧, projectを立ち上げる
def index(request):
    public = User.objects.get(username='public')
    # project一覧を取得
    projects = Project.objects.all()
    # projectを立ち上げる
    if request.method == 'POST':
        create_project_form = CreateProjectForm(request.POST)
        if create_project_form.is_valid():
            new_project = create_project_form.save(commit=False)
            new_project.owner = public
            new_project.save()
            return redirect(to='/media_uploader/')
    else:
        create_project_form = CreateProjectForm()
    
    params = {
        'projects': projects,
        'create_project_form': create_project_form,
    }
    return render(request, 'media_uploader/index.html', params)
    
# project詳細, fileをアップロード
def project(request, project_id):
    public = User.objects.get(username='public')
    # project詳細を取得
    project = Project.objects.get(id=project_id)
    files = File.objects.filter(project=project)
    # file uploader
    if request.method == 'POST':
        file_upload_form = FileUploadeForm(request.POST, request.FILES, project=project)
        if file_upload_form.is_valid():
            new_file = file_upload_form.save(commit=False)
            new_file.owner = public
            new_file.project = project
            new_file.save()
            return redirect(to=f'/media_uploader/project/{project_id}')
        else:
            print(file_upload_form.errors)
    else:
        file_upload_form = FileUploadeForm(project=project)
        
    params = {
        'project': project,
        'labels': project.labels,
        'files': files,
        'file_upload_form': file_upload_form,
    }
    return render(request, 'media_uploader/project.html', params)

def download(request, project_id):
    # プロジェクトとファイルを取得
    project = Project.objects.get(id=project_id)
    files = File.objects.filter(project=project_id)
    labels = project.labels
    
    # メモリ内のバッファを作成
    buffer = BytesIO()

    # ZIPファイルを作成
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            # ラベルごとのフォルダにファイルを配置
            folder_name = file.label # ラベルがない場合のデフォルト
            if folder_name > -1: # -1はundefined
                file_path_in_zip = f"{folder_name}/{labels[folder_name]}_{file.image.name.split('/')[-1]}"  # フォルダ名/ファイル名
            else:
                file_path_in_zip = f"unlabeled/unlabeled_{file.image.name.split('/')[-1]}"
            zip_file.writestr(file_path_in_zip, file.image.read())  # ファイルを追加

    # ZIPファイルをレスポンスに追加
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{project.title}.zip"'
    
    return response