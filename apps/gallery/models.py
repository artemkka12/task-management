from pathlib import Path

from django.contrib.auth.models import User
from django.db import models


def upload_to_user_id(instance: "Picture", filename: str) -> str:
    return Path(str(instance.user_id)).joinpath(filename).as_posix()


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to=upload_to_user_id)
