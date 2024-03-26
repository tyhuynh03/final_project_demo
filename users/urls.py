from django.urls import path
from .views import Register, loginView, LogoutView, UserDetailView, UserListView, home,register_view,home_content


urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("register-view/", register_view, name="register_view"),
    path("login/", loginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view() , name="logout"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail" ),
    path("user/", UserListView.as_view()),
    path("", home, name="login_view"),
    path("home-content/", home_content, name="home")
]
