from django.shortcuts import render,redirect
from .forms import QuestionForm, ChoiceFormSet
import csv
from .models import Question, Choice
from django.http import JsonResponse
import io
from .models import Question, Choice,Topic
from django.http import HttpResponseRedirect
from .serializers import QuestionSerializer, ChoiceSerializer, TopicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.contrib import messages
from .forms import TopicForm
from django.contrib.auth.decorators import login_required, user_passes_test

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'question_detail.html', {'question': question})

# thêm câu hỏi bằng thủ công
@login_required
def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and choice_formset.is_valid():
            topic_id = request.POST.get('topic_id')
            if topic_id:
                topic = Topic.objects.get(pk=topic_id)
            else:
                new_topic_name = request.POST.get('new_topic')
                topic, created = Topic.objects.get_or_create(name=new_topic_name, user=request.user)  # Gán người tạo chủ đề khi tạo mới
            question = question_form.save(commit=False)
            question.topic = topic
            question.save()
            choice_formset.instance = question
            choice_formset.save()
            return redirect('question_list')  # Điều hướng tới trang khác sau khi thêm câu hỏi và câu trả lời
    else:
        user = request.user
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()
        topic = Topic.objects.all()
    return render(request, 'add_question.html', {'question_form': question_form, 'choice_formset': choice_formset, 'topics': topic})

# def add_topic(request):
#     if request.method == 'POST':
        
#         form = TopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.user = request.user
#             topic.save()
#             form.save()
#             messages.success(request, 'Topic added successfully')
#             return redirect('topic_manage')  # Chuyển hướng đến trang homeadmin    
#     else:
#         form = TopicForm()
#     return render(request, 'topic_manage.html', {'form': form})



# thêm câu hỏi bằng file csv
def import_question_from_csv(request):
    if request.method == 'POST' and 'question_file' in request.FILES:
        file = request.FILES['question_file']
        if file.name.endswith('.csv'):
            csv_text_wrapper = io.TextIOWrapper(file, encoding='utf-8')
            reader = csv.reader(csv_text_wrapper)
            for row in reader:
                # Lấy thông tin từ hàng của tệp CSV
                topic_name = row[0]
                question_text = row[1]
                choices = row[2:]

                # Kiểm tra xem chủ đề đã tồn tại chưa, nếu không thì tạo mới
                topic, created = Topic.objects.get_or_create(name=topic_name)

                # Tạo câu hỏi và liên kết với chủ đề tương ứng
                question = Question.objects.create(text=question_text, topic=topic)

                # Tạo các lựa chọn cho câu hỏi
                for i in range(0, len(choices), 2):
                    choice_text = choices[i]
                    is_correct = choices[i + 1].lower() == 'true'
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

            return redirect('question_list')  # Chuyển hướng sau khi nhập dữ liệu thành công
        else:
            return JsonResponse({'error': 'Please upload a CSV file'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def home(request):
    topics = Topic.objects.all()
    for topic in topics:
        topic.question_count = topic.questions.count()
    return render(request, 'home.html', {'topics': topics})
@login_required
def start_quiz(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    questions = topic.questions.all()  # Truy vấn tất cả các câu hỏi liên quan đến chủ đề
    return render(request, 'quiz.html', {'topic': topic, 'questions': questions})

def add_question_csv(request):
    return render(request, 'add_question_csv.html')

# def submit_quiz(request):
#     if request.method == 'POST':
#         data = request.POST
#         correct_answers = 0
#         total_questions = 0
#         topic_id = request.POST.get('topic_id')  # Lấy ID của chủ đề từ biểu mẫu (nếu cần)
#         topic_questions = Question.objects.filter(topic_id=topic_id)  # Lọc câu hỏi theo chủ đề
#         for question in topic_questions:
#             total_questions += 1
#             # Lấy câu trả lời được chọn từ biểu mẫu
#             selected_choice_id = data.get(f'question{question.id}', None)
#             if selected_choice_id is not None:
#                 # Kiểm tra nếu selected_choice_id không phải là None
#                 selected_choice_id = int(selected_choice_id)
#                 selected_choice = Choice.objects.get(pk=selected_choice_id)
#                 if selected_choice.is_correct:
#                     correct_answers += 1
#         return render(request, 'quiz_result.html', {'correct_answers': correct_answers, 'total_questions': total_questions}) 
#     else:
#         return HttpResponseRedirect('/')
@login_required
def submit_quiz(request):
    if request.method == 'POST':
        data = request.POST
        correct_answers = 0;
        total_questions = 0;
        topic_id = request.POST.get('topic_id')
        topic_questions = Question.objects.filter(topic_id=topic_id)
        user_answers = []
        for question in topic_questions:
            total_questions += 1
            selected_choice_id = data.get(f'question{question.id}', None)
            if selected_choice_id is not None:
                selected_choice_id = int(selected_choice_id)
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                if selected_choice.is_correct:
                    correct_answers += 1
            
            user_answers.append({'question': question, 'selected_choice_id': selected_choice_id})
            
        return render(request, 'quiz_result.html', {'correct_answers': correct_answers, 'total_questions': total_questions, 'questions':topic_questions, 'user_answers':user_answers})
    else:
        return HttpResponseRedirect('/')
    

# quản lý câu hỏi
class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many =True)
        return Response(serializer.data)
def question_manage(request):
    response = requests.get(f'http://127.0.0.1:8000/questions')
    questions_data = response.json()
     # Truy vấn tất cả các chủ đề từ cơ sở dữ liệu
    topics = Topic.objects.all()

    # Tạo một từ điển để ánh xạ id của chủ đề vào tên của chúng
    topic_dict = {topic.id: topic.name for topic in topics}

    # Thay thế id của chủ đề bằng tên của chúng trong dữ liệu câu hỏi
    for question in questions_data:
        topic_id = question['topic']
        topic_name = topic_dict.get(topic_id, 'Unknown')
        question['topic_name'] = topic_name
    return render(request,'question_manage.html',{'questions_data':questions_data})
# quản lý chủ đề

@user_passes_test(lambda u: u.is_staff)
@login_required
def topic_manage(request):
    response = requests.get(f'http://127.0.0.1:8000/topics')
    topics_data = response.json()
    # truyền dữ liệu vào template và render trang
    return render(request, 'topic_manage.html', {'topics_data' : topics_data} )
def topic_detail(request, pk):
    response = TopicDetailView.as_view()(request, pk=pk)
    
    topic_data = response.data       
    return render(request, 'topic_detail.html', {'topic_data': topic_data})

def topic_update_view(request,topic_id):
    if request.method == "GET":
        response = requests.get(f'http://127.0.0.1:8000/topic/{topic_id}/')
        if response.status_code == 200:
            topic_data = response.json()
            return render(request, 'topic_update.html', {'topic_data': topic_data})
        else:
            # Xử lý trường hợp không tìm thấy người dùng
            messages.error(request, 'User not found')
            return redirect('topic_manage')
    elif request.method == 'POST':
        # Lấy dữ liệu từ form gửi lên
        updated_data = request.POST
        
        # Gửi yêu cầu Restapi để cập nhật thông tin
        response = requests.put(f'http://127.0.0.1:8000/topic/{topic_id}/', data=updated_data)
        if response.status_code == 200:
            messages.success(request, 'Topic information updated successfully')
            return redirect('topic_manage')
        else:
            # Xử lý trường hợp cập nhật thất bại
            messages.error(request, 'Failed to update Topic information')
            return redirect('topic_manage') 
@login_required
def add_topic(request):
    if request.method == 'POST':
        
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            form.save()
            messages.success(request, 'Topic added successfully')
            return redirect('topic_manage')  # Chuyển hướng đến trang homeadmin    
    else:
        form = TopicForm()
    return render(request, 'topic_manage.html', {'form': form})

class DeleteTopic(APIView):
    def delete(self, request, pk):
        topic = Topic.objects.filter(id=pk).first()
        if topic is None:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        topic.delete()
        return Response({"success": "Topic deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class TopicDetailView(APIView):
    def get(self,request,pk):
        topic = Topic.objects.filter(id=pk).first()
        if topic is None:
            return Response({"error":"Topic not found"},status=status.HTTP_404_NOT_FOUND)
        serialize = TopicSerializer(topic)
        return Response(serialize.data) 
    def put(self,request,pk):
        topic = Topic.objects.filter(id=pk).first()
        if topic is None:
            return Response({"error":"Topic not found"},status=status.HTTP_404_NOT_FOUND)
        serialize = TopicSerializer(topic,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class TopicListView(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many = True)
        return Response(serializer.data)