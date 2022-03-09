from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.tasks.models import Task, Timelog


class Command(BaseCommand):
    help = 'Command for create 25000 tasks'

    def handle(self, *args, **options):
        fake = Faker()
        user = User.objects.get(pk=1)
        for i in range(25000):
            task = Task.objects.create(
                title=fake.name(),
                description=fake.text(),
                completed=False,
                owner=user
            )

            task.save()

            timelog = Timelog.objects.create(
                task=task,
                owner=user,
                started_at=timezone.now(),
                stopped_at=timezone.now() + timezone.timedelta(seconds=2),
            )
            timelog.duration = timelog.stopped_at - timelog.started_at
            timelog.save()
