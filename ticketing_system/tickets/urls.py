from django.urls import path,include
from rest_framework.routers import SimpleRouter
from .views import TicketViewSet

router = SimpleRouter()
router.register('ticket',TicketViewSet)

app_name = 'tickets'

urlpatterns = []

urlpatterns += router.urls