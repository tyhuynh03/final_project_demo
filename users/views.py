from django.shortcuts import render, redirect
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
# Create your views here.

class Register(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, 'Account created successfully')
        return HttpResponseRedirect(reverse('home_login'))

class loginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')    
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        return HttpResponseRedirect(reverse('home'))
    

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return HttpResponseRedirect(reverse('home_login'))
class UserDetailView(APIView):
    def get(self,request,pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

def home(request):
    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    return render(request, 'register.html')
def home_content(request):
    return render(request, 'quiz.html')

