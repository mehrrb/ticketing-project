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
    
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return LoginSerializer
        else:
            return UserSerializer
    
    
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
