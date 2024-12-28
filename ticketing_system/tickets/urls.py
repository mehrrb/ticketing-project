from django.urls import path,include
from rest_framework.routers import SimpleRouter
from .views import TicketViewSet, CategoryViewSet, NotificationViewSet

router = SimpleRouter()
router.register('ticket',TicketViewSet)
router.register('categories',CategoryViewSet)
router.register('notifications',NotificationViewSet,basename='notification')

app_name = 'tickets'

urlpatterns = []

urlpatterns += router.urls