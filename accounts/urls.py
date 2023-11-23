from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('sing-in/', LoginUserView.as_view(), name='sing_in'),
    path('check_username/', CheckUsername.as_view(), name='check_username'),
    path('sing-up/', CreateUser.as_view(), name='sing_up'),
    path('logout/', logout_user, name='logout'),
    path('change-password/', UserPasswordChange.as_view(), name='user-change-password'),
    path('list-community/<str:following_or_followers>/',
         ListCommunityView.as_view(), name='user-community'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
        email_template_name='accounts/password_reset_email.html'),
        name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path(
        '<slug:user_slug>/',
        include(
            [
                path('settings/', login_required(UserSettingsView.as_view()), name='user-settings'),
                path('profile/', login_required(UserProfileView.as_view()), name='user-profile'),
                path('update/', UserUpdateView.as_view(), name='user-update'),
                path('follow-user/', FollowUser.as_view(), name='user-follow'),
                path('update/banner/', UpdateBannerProfile.as_view(), name='user-update-banner'),

            ]
        ),
    ),
]
