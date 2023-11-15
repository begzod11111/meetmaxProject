from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('sing-in/', LoginUserView.as_view(), name='sing_in'),
    path('check_username/', CheckUsername.as_view(), name='check_username'),
    path('sing-up/', CreateUser.as_view(), name='sing_up'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html'),
        name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path(
        '<slug:user_slug>/',
        include(
            [
                path('profile/', UserProfileView.as_view(), name='user-profile'),
                path("settings/", UserSettingsView.as_view(), name='user-settings'),
                path('update/', UserUpdateView.as_view(), name='user-update'),
                path('change-password/', UserPasswordChange.as_view(), name='user-change-password'),
                path('logout/', logout_user, name='logout'),
                path('follow-user/', FollowUser.as_view(), name='user-follow'),
                path('list-community/<str:following_or_followers>/',
                     ListCommunityView.as_view(), name='user-community')
            ]
        ),
    ),
]
