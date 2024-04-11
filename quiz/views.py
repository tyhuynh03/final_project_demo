from django.shortcuts import render,redirect
from .forms import QuestionForm, ChoiceForm
from .forms import QuestionForm, ChoiceFormSet
import csv
from .models import Question, Choice
from django.http import JsonResponse
import io
from .models import Question, Choice,Topic
from django.http import HttpResponseRedirect

def question_list(request):
    questions = Question.objects.all()
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


def question_test(request):
    questions = Question.objects.all()
    return render(request, 'question_test.html', {'questions': questions})
def home(request):
    topics = Topic.objects.all()
    for topic in topics:
        topic.question_count = topic.questions.count()
    return render(request, 'home.html', {'topics': topics})

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
    
