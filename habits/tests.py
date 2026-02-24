from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тестирование создания привычки"""

        data = {
            "place": "Дом",
            "time": "12:00",
            "action": "Тест",
            "duration": 60,
            "periodicity": 1,
            "is_public": False,
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertTrue(Habit.objects.all().exists())

    def test_list_habit(self):
        """Тестирование получения списка привычек пользователя"""

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_habit(self):
        """Тестирование получения детальной информации о привычке"""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00",
            action="Читать книгу",
            duration=60,
            periodicity=1,
            is_public=False,
        )

        response = self.client.get(f"/habits/{habit.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Читать книгу")
        self.assertEqual(response.data["place"], "Дом")

    def test_cannot_retrieve_foreign_habit(self):
        """Тестирование запрета получения чужой привычки."""

        other_user = User.objects.create_user(username="otheruser", password="1234")

        habit = Habit.objects.create(
            user=other_user,
            place="Офис",
            time="10:00",
            action="Пить воду",
            duration=30,
            periodicity=1,
            is_public=False,
        )

        response = self.client.get(f"/habits/{habit.id}/")

        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    def test_update_own_habit(self):
        """Тестирование обновления привычки пользователя"""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00",
            action="Старая привычка",
            duration=60,
            periodicity=1,
            is_public=False,
        )

        response = self.client.patch(
            f"/habits/{habit.id}/", {"action": "Новая привычка"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Новая привычка")

    def test_delete_own_habit(self):
        """Тестирование удаления привычки пользователя"""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00",
            action="Удалить меня",
            duration=60,
            periodicity=1,
            is_public=False,
        )

        response = self.client.delete(f"/habits/{habit.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_periodicity_limit_validation(self):
        """Тестирование ограничения периодичности привычки"""

        data = {
            "place": "Дом",
            "time": "12:00",
            "action": "Бег",
            "duration": 60,
            "periodicity": 10,  # больше 7
            "is_public": False,
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_limit_validation(self):
        """Тестирование ограничения длительности привычки"""

        data = {
            "place": "Дом",
            "time": "12:00",
            "action": "Читать",
            "duration": 150,  # больше 120
            "periodicity": 1,
            "is_public": False,
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reward_and_related_habit_validation(self):
        """Тестирование запрета одновременного указания вознаграждения и связанной привычки"""

        related_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="10:00",
            action="Базовая привычка",
            duration=60,
            periodicity=1,
            is_public=False,
        )

        data = {
            "place": "Дом",
            "time": "12:00",
            "action": "Новая привычка",
            "duration": 60,
            "periodicity": 1,
            "reward": "Шоколад",
            "related_habit": related_habit.id,
            "is_public": False,
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
