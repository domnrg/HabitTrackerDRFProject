from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="1234"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """ Тестирование создания привычки """

        data = {
            "place": "Дом",
            "time": "12:00",
            "action": "Тест",
            "duration": 60,
            "periodicity": 1,
            "is_public": False
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertTrue(Habit.objects.all().exists())

    def test_list_habit(self):
        """ Тестирование получения списка привычек пользователя """

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

