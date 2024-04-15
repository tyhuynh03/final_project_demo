from django.urls import path
from . import views

urlpatterns = [
    path('question_list/', views.question_list, name='question_list'),
    path('question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('import_question_from_csv/', views.import_question_from_csv, name='import_questions_csv'),
    path('add_question/', views.add_question, name='add_question'),
    path('', views.home, name='home'),
    path('start-quiz/<int:topic_id>/', views.start_quiz, name='start_quiz'),
    path("add_question_csv/",views.add_question_csv,name="add_question_csv"),
    path("submit_quiz/",views.submit_quiz,name="submit_quiz"),
    path("topic/<int:pk>/", views.TopicDetailView.as_view(), name="topicdetail" ),
    path("topics/", views.TopicListView.as_view(), name="topics" ),
    path("topic_manage/",views.topic_manage,name="topic_manage"),
    path("questions/",views.QuestionListView.as_view(),name = 'questions'),
    path("topic_detail/<int:pk>/",views.topic_detail,name = 'topic_detail'),
    path("topic_update/<int:topic_id>/",views.topic_update_view,name="topic_update"),
    path("add_topic/",views.add_topic,name="add_topic"),
    path('delete_topic/<int:pk>/', views.DeleteTopic.as_view(), name='delete_topic'),
    path("question_manage/",views.question_manage,name = "question_manage")
]   
