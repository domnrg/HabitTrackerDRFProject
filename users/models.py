from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Telegram chat ID"
    )

    def __str__(self):
        return self.username
