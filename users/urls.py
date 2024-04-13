from django.urls import path
from .views import Register, loginView, LogoutView, UserDetailView, UserListView
from .views import home,register_view,home_content,login_view,  info_page, HomeAdminView,add_user,DeleteUser,user_detail,user_update_view,DashboardView, MyPageView

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("register-view/", register_view, name="register_view"),
    path("login/", loginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view() , name="logout"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="userdetail" ),
    path("user_detail/<int:pk>/", user_detail, name="user_detail"),
    path("user/", UserListView.as_view(), name= 'user'),
    path("", home, name="home"),
    path("home-content/", home_content, name="home_content"),
    path("login-view/", login_view, name="login_view"),
    path('info/', info_page, name='info_page'),
    path("home_admin/",HomeAdminView.as_view(), name = "home_admin" ),
    path("add_user/",add_user,name = "add_user"),
    path('delete_user/<int:pk>/', DeleteUser.as_view(), name='delete_user'),
    path('update-user/<int:user_id>/', user_update_view, name='user_update'),
    path("dashboard/",DashboardView.as_view(), name= "dashboard"),
    path("mypage/",MyPageView.as_view(),name = "my_page")

    

]
