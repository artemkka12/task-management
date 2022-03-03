from django.core.management import BaseCommand
from apps.tasks.models import Task


class Command(BaseCommand):
    help = 'Command for delete all tasks'

    def handle(self, *args, **options):
        Task.objects.all().delete()
