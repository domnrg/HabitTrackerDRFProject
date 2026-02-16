from rest_framework.serializers import ValidationError


def validate_habit(data):
    is_pleasant = data.get('is_pleasant')
    reward = data.get('reward')
    related_habit = data.get('related_habit')
    duration = data.get('duration')

    if duration > 2:
        raise ValidationError('Время выполнения привычки не должно превышать 120 секунд.')

    if reward and related_habit:
        raise ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку.')

    if is_pleasant and reward:
        raise ValidationError('Приятная привычка не может иметь вознаграждение.')

    if related_habit and not related_habit.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')

    if is_pleasant and related_habit:
        raise ValidationError('Приятная привычка не может иметь связанную привычку.')
