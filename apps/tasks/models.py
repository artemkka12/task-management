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
    started_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta())

    def __str__(self):
        return f'{self.task}'


class Timer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
            duration = timezone.now() - self.started_at
            self.duration += duration
            self.started_at = self.started_at
            self.is_running = False
            self.save()

            timelog = Timelog.objects.create(
                task=self.task,
                owner=self.owner,
                started_at=self.started_at,
                stopped_at=timezone.now(),
                duration=duration
            )

            timelog.save()

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
