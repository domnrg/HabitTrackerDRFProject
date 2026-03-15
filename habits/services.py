import requests
from django.conf import settings


def send_telegram_message(chat_id: int, message: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"

    data = {"chat_id": chat_id, "text": message}

    requests.post(url, data=data)
