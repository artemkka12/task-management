from django.core.management import BaseCommand, CommandError

from apps.tasks.models import Task


class Command(BaseCommand):
    help = 'Command for get a task by id'

    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='+', type=int)

        parser.add_argument('--delete',
                            action='store_true',
                            help='Delete task instead od completing it'
                            )

    def handle(self, *args, **options):

        for task_id in options['task_ids']:
            try:
                task = Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)

            task.completed = True
            task.save()

            self.stdout.write(self.style.SUCCESS('Successfully completed task "%s"' % task_id))
