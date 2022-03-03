import time

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from faker import Faker

from apps.tasks.models import Task, Timer


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
            timer = Timer.objects.create(task=task, owner=user)
            timer.save()
            timer.start()
            time.sleep(0.0001)
            timer.pause()
            timer.start()
            time.sleep(0.0002)
            timer.stop()
