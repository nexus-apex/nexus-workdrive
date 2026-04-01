import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Folder, StoredFile, ShareLink


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['folder_count'] = Folder.objects.count()
    ctx['folder_total_size_mb'] = Folder.objects.aggregate(t=Sum('size_mb'))['t'] or 0
    ctx['storedfile_count'] = StoredFile.objects.count()
    ctx['storedfile_document'] = StoredFile.objects.filter(file_type='document').count()
    ctx['storedfile_image'] = StoredFile.objects.filter(file_type='image').count()
    ctx['storedfile_video'] = StoredFile.objects.filter(file_type='video').count()
    ctx['storedfile_total_size_mb'] = StoredFile.objects.aggregate(t=Sum('size_mb'))['t'] or 0
    ctx['sharelink_count'] = ShareLink.objects.count()
    ctx['sharelink_view'] = ShareLink.objects.filter(permission='view').count()
    ctx['sharelink_edit'] = ShareLink.objects.filter(permission='edit').count()
    ctx['sharelink_download'] = ShareLink.objects.filter(permission='download').count()
    ctx['recent'] = Folder.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def folder_list(request):
    qs = Folder.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = ''
    return render(request, 'folder_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def folder_create(request):
    if request.method == 'POST':
        obj = Folder()
        obj.name = request.POST.get('name', '')
        obj.parent_path = request.POST.get('parent_path', '')
        obj.owner = request.POST.get('owner', '')
        obj.files_count = request.POST.get('files_count') or 0
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.shared = request.POST.get('shared') == 'on'
        obj.created_date = request.POST.get('created_date') or None
        obj.save()
        return redirect('/folders/')
    return render(request, 'folder_form.html', {'editing': False})


@login_required
def folder_edit(request, pk):
    obj = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.parent_path = request.POST.get('parent_path', '')
        obj.owner = request.POST.get('owner', '')
        obj.files_count = request.POST.get('files_count') or 0
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.shared = request.POST.get('shared') == 'on'
        obj.created_date = request.POST.get('created_date') or None
        obj.save()
        return redirect('/folders/')
    return render(request, 'folder_form.html', {'record': obj, 'editing': True})


@login_required
def folder_delete(request, pk):
    obj = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/folders/')


@login_required
def storedfile_list(request):
    qs = StoredFile.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(file_type=status_filter)
    return render(request, 'storedfile_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def storedfile_create(request):
    if request.method == 'POST':
        obj = StoredFile()
        obj.name = request.POST.get('name', '')
        obj.folder_path = request.POST.get('folder_path', '')
        obj.file_type = request.POST.get('file_type', '')
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.uploaded_by = request.POST.get('uploaded_by', '')
        obj.uploaded_date = request.POST.get('uploaded_date') or None
        obj.shared = request.POST.get('shared') == 'on'
        obj.download_url = request.POST.get('download_url', '')
        obj.save()
        return redirect('/storedfiles/')
    return render(request, 'storedfile_form.html', {'editing': False})


@login_required
def storedfile_edit(request, pk):
    obj = get_object_or_404(StoredFile, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.folder_path = request.POST.get('folder_path', '')
        obj.file_type = request.POST.get('file_type', '')
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.uploaded_by = request.POST.get('uploaded_by', '')
        obj.uploaded_date = request.POST.get('uploaded_date') or None
        obj.shared = request.POST.get('shared') == 'on'
        obj.download_url = request.POST.get('download_url', '')
        obj.save()
        return redirect('/storedfiles/')
    return render(request, 'storedfile_form.html', {'record': obj, 'editing': True})


@login_required
def storedfile_delete(request, pk):
    obj = get_object_or_404(StoredFile, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/storedfiles/')


@login_required
def sharelink_list(request):
    qs = ShareLink.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(file_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(permission=status_filter)
    return render(request, 'sharelink_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def sharelink_create(request):
    if request.method == 'POST':
        obj = ShareLink()
        obj.file_name = request.POST.get('file_name', '')
        obj.shared_by = request.POST.get('shared_by', '')
        obj.shared_with = request.POST.get('shared_with', '')
        obj.permission = request.POST.get('permission', '')
        obj.expires = request.POST.get('expires') or None
        obj.access_count = request.POST.get('access_count') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/sharelinks/')
    return render(request, 'sharelink_form.html', {'editing': False})


@login_required
def sharelink_edit(request, pk):
    obj = get_object_or_404(ShareLink, pk=pk)
    if request.method == 'POST':
        obj.file_name = request.POST.get('file_name', '')
        obj.shared_by = request.POST.get('shared_by', '')
        obj.shared_with = request.POST.get('shared_with', '')
        obj.permission = request.POST.get('permission', '')
        obj.expires = request.POST.get('expires') or None
        obj.access_count = request.POST.get('access_count') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/sharelinks/')
    return render(request, 'sharelink_form.html', {'record': obj, 'editing': True})


@login_required
def sharelink_delete(request, pk):
    obj = get_object_or_404(ShareLink, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/sharelinks/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['folder_count'] = Folder.objects.count()
    data['storedfile_count'] = StoredFile.objects.count()
    data['sharelink_count'] = ShareLink.objects.count()
    return JsonResponse(data)
