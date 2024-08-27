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
    
    
    def post(self,request):
        try:
            
            email = request.data.get('email')
            password = request.data.get('password')
            user = Users.objects.get(email=email)
            check_password = user.check_password(password)
            if check_password:
                ser_user = LoginSerializer(data=request.data)
                if ser_user.is_valid():
                    token = RefreshToken.for_user(user)
                    access_token = str(token.access_token)
                    refresh_token = str(token)
                    login(request, user)
                    response = {}
                    response = ser_user.data
                    response['access_token'] = access_token
                    response['refresh_token'] = refresh_token
                    if user.is_superuser:
                        response['is_superuser'] = True  
                    else:
                        response['is_superuser'] = False
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(ser_user.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({"error": "user not valid"}, status=status.HTTP_400_BAD_REQUEST)
        


#    
# def post(request):


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
