from rest_framework import viewsets, permissions,status
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from rest_framework.response import Response
from .serializers import TicketSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action




class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
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
            title = serialized_data.validated_data['title']
            description = serialized_data.validated_data['description']
            ticket = Ticket(
                user = user,
                title = title,
                description = description
            )
            ticket.save()
            return Response({'info': 'successfully created!'},status=status.HTTP_201_CREATED)
            
        else:
            return Response(serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        user = request.user
        
        if user.is_superuser:
            ticket.is_read_by_admin = True
            ticket.reply = request.data.get('reply', None)
        else:
            if not ticket.reply:
                return Response({'error':'wait for admin...'},status=status.HTTP_204_NO_CONTENT)
        
        serialized_data = TicketSerializer(ticket,data=request.data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            
            return Response({'cool':'updated successfully'}, status=status.HTTP_200_OK)
        
        else:
            return Response(serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
