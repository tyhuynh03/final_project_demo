from django.urls import path
from . import views

urlpatterns = [
    path('question_list/', views.question_list, name='question_list'),
    path('question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('import_question_from_csv/', views.import_question_from_csv, name='import_questions_csv'),
    path('add_question/', views.add_question, name='add_question'),
    path("test/",views.question_test,name="question_test"),
    path('', views.home, name='home'),
    path('start-quiz/<int:topic_id>/', views.start_quiz, name='start_quiz'),
    path("add_question_csv/",views.add_question_csv,name="add_question_csv"),
    path("submit_quiz/",views.submit_quiz,name="submit_quiz")
]   
