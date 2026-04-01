from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Folder, StoredFile, ShareLink
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusWorkDrive with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusworkdrive.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Folder.objects.count() == 0:
            for i in range(10):
                Folder.objects.create(
                    name=f"Sample Folder {i+1}",
                    parent_path=f"Sample {i+1}",
                    owner=f"Sample {i+1}",
                    files_count=random.randint(1, 100),
                    size_mb=round(random.uniform(1000, 50000), 2),
                    shared=random.choice([True, False]),
                    created_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 Folder records created'))

        if StoredFile.objects.count() == 0:
            for i in range(10):
                StoredFile.objects.create(
                    name=f"Sample StoredFile {i+1}",
                    folder_path=f"Sample {i+1}",
                    file_type=random.choice(["document", "image", "video", "audio", "archive"]),
                    size_mb=round(random.uniform(1000, 50000), 2),
                    uploaded_by=f"Sample {i+1}",
                    uploaded_date=date.today() - timedelta(days=random.randint(0, 90)),
                    shared=random.choice([True, False]),
                    download_url=f"https://example.com/{i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 StoredFile records created'))

        if ShareLink.objects.count() == 0:
            for i in range(10):
                ShareLink.objects.create(
                    file_name=f"Sample ShareLink {i+1}",
                    shared_by=f"Sample {i+1}",
                    shared_with=f"Sample {i+1}",
                    permission=random.choice(["view", "edit", "download"]),
                    expires=date.today() - timedelta(days=random.randint(0, 90)),
                    access_count=random.randint(1, 100),
                    active=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 ShareLink records created'))
