from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место'
    )

    time = models.TimeField(
        verbose_name='Время'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )

    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )

    duration = models.PositiveSmallIntegerField(
        verbose_name='Время выполнения (в минутах)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'
