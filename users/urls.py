from django.urls import path
from .views import Register, loginView, LogoutView, UserDetailView, UserListView, home,register_view,home_content,login_view, my_page


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
    path("mypage/", my_page, name="my_page")

]
