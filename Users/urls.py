from django.urls import path
from .views import RegisterView, LoginView, LogoutView, AllUsersView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view()),
    path('users/',AllUsersView.as_view()),
    path('user/details', UserDetailView.as_view()),
]
