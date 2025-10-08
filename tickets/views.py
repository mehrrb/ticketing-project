from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Notification, Ticket
from .serializers import CategorySerializer, NotificationSerializer, TicketSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "notification marked as read"})


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["description", "title"]
    filterset_fields = ["status", "priority"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return Ticket.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serialized_data = TicketSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.validated_data["user"] = user
            serialized_data.save()
            return Response(
                {"info": "successfully created!"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        user = request.user

        if user.is_superuser:
            ticket.is_read_by_admin = True
            serialized_data = TicketSerializer(ticket, data=request.data, partial=True)
            if serialized_data.is_valid():
                ticket = serialized_data.save()
                return Response(
                    {"info": "updated successfully"}, status=status.HTTP_200_OK
                )
        else:
            if not ticket.reply:
                return Response(
                    {"error": "wait for admin..."}, status=status.HTTP_204_NO_CONTENT
                )

        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        old_status = self.get_object().status
        ticket = serializer.save()

        if old_status != ticket.status:
            Notification.objects.create(
                user=ticket.user,
                ticket=ticket,
                notification_type="status_change",
                message=f"Ticket status changed to {ticket.get_status_display()}",
            )
