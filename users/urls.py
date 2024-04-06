from django.urls import path
from .views import Register, loginView, LogoutView, UserDetailView, UserListView, question_list, question_detail, import_question_from_csv, add_question,delete_question
from .views import home,register_view,home_content,login_view, my_page, info_page

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("register-view/", register_view, name="register_view"),
    path("login/", loginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view() , name="logout"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail" ),
    path("user/", UserListView.as_view(), name= 'user'),
    path("", home, name="home"),
    path("home-content/", home_content, name="home_content"),
    path("login-view/", login_view, name="login_view"),
    path("mypage/", my_page, name="my_page"),
    path('question_list/', question_list, name='question_list'),
    path('question_detail/<int:question_id>/', question_detail, name='question_detail'),
    path('import_question_from_csv/', import_question_from_csv, name='import_questions_csv'),
    path('add_question/', add_question, name='add_question'),
    path('delete_question/<int:question_id>/', delete_question, name='delete_question'),
    path('info/', info_page, name='info_page')

]
