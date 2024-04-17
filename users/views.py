from django.shortcuts import render, redirect
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from rest_framework import status
from django.urls import reverse
from django.contrib import messages
from quiz.models import Topic,Question
from django.shortcuts import redirect
from users.forms import UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import requests
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test

class Register(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, 'Account created successfully')
        # sau khi tạo tài khoản xong thì load lại trang đang ở
        return redirect(reverse('login_view'))




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
        login(request, user)
        # Kiểm tra nếu người dùng là admin
        if user.is_staff:
            # Nếu là admin, chuyển hướng đến trang homeadmin
            return redirect('home_admin')
        else:
            # Nếu không phải admin, chuyển hướng đến trang my_page
            return redirect('my_page')


       
    

class LogoutView(APIView):
    def post(self,request):
        logout(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': ' logout success'
        }
        return render(request,'login.html')
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

def info_page(request):
    return render(request, 'info.html')



class DeleteUser(APIView):
    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"success": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully')
            return redirect('home_admin')  # Chuyển hướng đến trang homeadmin
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})
def user_detail(request, pk):
    # Gọi REST API để lấy thông tin chi tiết của người dùng
    response = requests.get(f'http://127.0.0.1:8000/user/{pk}/')
    user_data = response.json()
    # Truyền dữ liệu vào template và render trang
    return render(request, 'user_detail.html', {'user_data': user_data})


def user_update_view(request, user_id):
    # Xử lý yêu cầu GET để hiển thị form cập nhật thông tin người dùng
    if request.method == 'GET':
        # Gửi yêu cầu REST API để lấy thông tin chi tiết của người dùng
        response = requests.get(f'http://127.0.0.1:8000/user/{user_id}/')
        if response.status_code == 200:
            user_data = response.json()
            return render(request, 'user_update.html', {'user_data': user_data})
        else:
            # Xử lý trường hợp không tìm thấy người dùng
            messages.error(request, 'User not found')
            return redirect('home_admin')
    # Xử lý yêu cầu POST để cập nhật thông tin người dùng
    elif request.method == 'POST':
        # Lấy dữ liệu từ form gửi lên
        updated_data = request.POST
        # Gửi yêu cầu REST API để cập nhật thông tin người dùng
        response = requests.put(f'http://127.0.0.1:8000/user/{user_id}/', data=updated_data)
        if response.status_code == 200:
            messages.success(request, 'User information updated successfully')
            return redirect('home_admin')
        else:
            # Xử lý trường hợp cập nhật thất bại
            messages.error(request, 'Failed to update user information')
            return redirect('home_admin')    

class HomeAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        users = User.objects.all()
        return render(request, 'home_admin.html', {'users': users})
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #lấy ra tổng user và tổng topic tổng câu hỏi
        total_user = User.objects.all().count()
        total_topic = Topic.objects.all().count()
        total_questions = Question.objects.all().count()

        context['total_user'] = total_user
        context['total_topic'] = total_topic
        context['total_questions'] = total_questions

        return context
class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        topics = Topic.objects.all()
        for topic in topics:
            topic.question_count = topic.questions.count()
            topic.created_by = topic.user.username
        context['topics'] = topics
        context['current_user'] = current_user.username
        return context

