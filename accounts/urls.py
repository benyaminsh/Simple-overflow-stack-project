from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='user_profile'),
    path('reset/', views.PasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('configrm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('configrm/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UnfollowView.as_view(), name='user_unfollow'),
    path('edit_user/', views.EditUserView.as_view(), name='edit_user'),
]