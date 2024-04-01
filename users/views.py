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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.shortcuts import redirect
from django.urls import reverse

class loginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Thực hiện xác thực người dùng
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        return redirect(reverse('my_page')) 

        
    

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': ' logout success'
        }
        return response
class UserDetailView(APIView):
    def get(self,request,pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def put(self,request,pk):   
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Cập nhật dữ liệu người dùng từ các tham số truyền vào
        if 'username' in request.data:
            user.username = request.data['username']
        if 'email' in request.data:
            user.email = request.data['email']
        # Thêm các trường khác cần cập nhật nếu có

        # Lưu lại thay đổi
        user.save()

        # Tạo serializer với dữ liệu người dùng đã được cập nhật
        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

def home(request):
    return render(request, 'home.html')
def register_view(request):
    return render(request, 'register.html')
def home_content(request):
    return render(request, 'quiz.html')
def login_view(request):
    return render(request, 'login.html')
def my_page(request):
    return render(request, 'mypage.html')

class DeleteUser(APIView):
    def delete(self,request,pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)