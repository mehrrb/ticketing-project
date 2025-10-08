from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import Users
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
import logging
import traceback
import os


class UsersView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer    

    def create(self, request, *args, **kwargs):
        data = request.data
        ser_data = UserSerializer(data=data)
        if ser_data.is_valid():
            email = ser_data.validated_data['email']
            password = ser_data.validated_data['password']
            
            user = Users(
                email = email,            
            )
            user.set_password(password)
            user.save()
            return Response({"info" : "successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class LoginView(APIView):
    
    
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or not password:
                return Response(
                    {"error": "Email and password are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if '@' not in email or '.' not in email:
                return Response(
                    {"error": "Invalid email format"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.check_password(password):
                return Response(
                    {"error": "Invalid credentials"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Validate serializer
            ser_user = LoginSerializer(data=request.data)
            if not ser_user.is_valid():
                return Response(ser_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate tokens
            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
            
            # Login user
            login(request, user)
            
            # Prepare response
            response = ser_user.data.copy()
            response['access_token'] = access_token
            response['refresh_token'] = refresh_token
            response['is_superuser'] = user.is_superuser
            
            return Response(response, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log the actual error for debugging (only in development)
            if os.getenv('DEBUG', 'False').lower() == 'true':
                logging.error(f"Login error: {str(e)}")
                logging.error(traceback.format_exc())
            
            # Return generic error to user
            return Response(
                {"error": "Authentication failed"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


#    
# def post(request):


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
