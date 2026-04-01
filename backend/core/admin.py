from django.contrib import admin
from .models import Folder, StoredFile, ShareLink

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ["name", "parent_path", "owner", "files_count", "size_mb", "created_at"]
    search_fields = ["name", "parent_path", "owner"]

@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ["name", "folder_path", "file_type", "size_mb", "uploaded_by", "created_at"]
    list_filter = ["file_type"]
    search_fields = ["name", "folder_path", "uploaded_by"]

@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ["file_name", "shared_by", "shared_with", "permission", "expires", "created_at"]
    list_filter = ["permission"]
    search_fields = ["file_name", "shared_by", "shared_with"]
