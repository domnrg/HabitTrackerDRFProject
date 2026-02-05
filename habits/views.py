from rest_framework import viewsets

from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer



