from rest_framework.routers import SimpleRouter

from habits.views import HabitViewSet, PublicHabitViewSet
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = SimpleRouter()
router.register('', HabitViewSet, basename='habit')
router.register('public-habits', PublicHabitViewSet, basename='public-habit')

urlpatterns = router.urls

