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
def info_page(request):
    return render(request, 'info.html')

class DeleteUser(APIView):
    def delete(self,request,pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
    
from django.shortcuts import render,redirect
from .forms import QuestionForm, ChoiceForm
from django.shortcuts import render, redirect
from .forms import QuestionForm, ChoiceFormSet
import csv
from django.shortcuts import render
from .models import Question, Choice
from django.core.files.uploadedfile import UploadedFile
from rest_framework.response import Response
from django.http import JsonResponse
    
# def question_list(request):
#     questions = Question.objects.all()
#     return render(request, 'question_list.html', {'questions': questions})
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})

    return render(request, 'question_list.html', {'questions': questions})
def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'question_detail.html', {'question': question})

def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save()
            choice_formset.instance = question
            choice_formset.save()
            return redirect('question_list')  # Điều hướng tới trang khác sau khi thêm câu hỏi và câu trả lời
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()
    return render(request, 'add_question.html', {'question_form': question_form, 'choice_formset': choice_formset})
from django.shortcuts import redirect
from .models import Question

def delete_question(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        question.delete()
        return redirect('question_list')



from django.shortcuts import redirect
import csv
from .models import Question, Choice

import io
import csv
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Question, Choice

def import_question_from_csv(request):
    if request.method == 'POST' and 'question_file' in request.FILES:
        file = request.FILES['question_file']
        if file.name.endswith('.csv'):
            csv_text_wrapper = io.TextIOWrapper(file, encoding='utf-8')
            reader = csv.reader(csv_text_wrapper)
            for row in reader:
                question_text = row[0]
                question = Question.objects.create(text=question_text)
                for i in range(1, len(row), 2):
                    choice_text = row[i]
                    is_correct = row[i + 1].lower() == 'true'
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
            return redirect('question_list')  # Chuyển hướng sau khi nhập dữ liệu thành công
        else:
            return JsonResponse({'error': 'Please upload a CSV file'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


