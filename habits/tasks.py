from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from telegram_bot.services import send_telegram_message


@shared_task
def check_habits():
    now = timezone.localtime()

    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
        user__telegram_chat_id__isnull=False
    )

    for habit in habits:
        message = f"Пора выполнить привычку: {habit.action}"
        send_telegram_message(
            habit.user.telegram_chat_id,
            message
        )

    print("HABITS FOUND:", habits.count())

    for habit in habits:
        print("SENDING:", habit.action)
        message = f"Пора выполнить привычку: {habit.action}"
        send_telegram_message(
            habit.user.telegram_chat_id,
            message
        )
