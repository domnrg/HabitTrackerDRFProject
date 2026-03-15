from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):

        is_pleasant = data.get("is_pleasant")
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        duration = data.get("duration")

        if duration and duration > 120:
            raise serializers.ValidationError(
                {
                    "duration": "Время выполнения привычки не должно превышать 120 секунд."
                }
            )

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if is_pleasant and reward:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if is_pleasant and related_habit:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь связанную привычку."
            )

        return data
