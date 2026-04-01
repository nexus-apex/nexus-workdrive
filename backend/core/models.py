from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_path = models.CharField(max_length=255, blank=True, default="")
    owner = models.CharField(max_length=255, blank=True, default="")
    files_count = models.IntegerField(default=0)
    size_mb = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shared = models.BooleanField(default=False)
    created_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class StoredFile(models.Model):
    name = models.CharField(max_length=255)
    folder_path = models.CharField(max_length=255, blank=True, default="")
    file_type = models.CharField(max_length=50, choices=[("document", "Document"), ("image", "Image"), ("video", "Video"), ("audio", "Audio"), ("archive", "Archive")], default="document")
    size_mb = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    uploaded_by = models.CharField(max_length=255, blank=True, default="")
    uploaded_date = models.DateField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    download_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ShareLink(models.Model):
    file_name = models.CharField(max_length=255)
    shared_by = models.CharField(max_length=255, blank=True, default="")
    shared_with = models.CharField(max_length=255, blank=True, default="")
    permission = models.CharField(max_length=50, choices=[("view", "View"), ("edit", "Edit"), ("download", "Download")], default="view")
    expires = models.DateField(null=True, blank=True)
    access_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name
