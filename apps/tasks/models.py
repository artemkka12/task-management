from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'{self.title}'


class Timelog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task}'


class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_stopped = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    duration = models.DurationField(default=timedelta())

    def start(self):
        if self.is_stopped:
            raise ValueError("Timer is stopped")

        if not self.is_running:
            self.started_at = timezone.now()
            self.is_running = True
            self.save()

    def pause(self):
        if self.is_stopped:
            raise ValueError("Timer is stopped")

        if self.is_running:
            self.duration += timezone.now() - self.started_at
            self.started_at = None
            self.is_running = False
            self.save()

            # Todo: create Timelog

    def reset(self):
        if self.is_stopped:
            raise ValueError("Timer is stopped")

        self.is_running = False
        self.is_stopped = False
        self.started_at = None
        self.duration = timedelta()
        self.save()

    def stop(self):
        if self.is_stopped:
            raise ValueError("Timer is stopped")

        self.pause()
        self.is_stopped = True
        self.save()

    @property
    def total_duration(self):
        now = timezone.now()
        return self.duration + ((now - (self.started_at or now)) * int(self.is_running))
