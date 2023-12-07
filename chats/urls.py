from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'chats'

urlpatterns = [
	path('<str:type_chats>/all/', login_required(DialogsUserView.as_view()), name='chats'),
	path('<str:type_chats>/<str:companion_slug>/', login_required(DialogsUserView.as_view()), name='personal_chat_dialog'),
	path('check-satus/', CheckOnlineUser.as_view(), name='check-satus'),
	path('add-dch/', AddDCHView.as_view(), name='add-dchat'),
	path('add-chat/', AddChatView.as_view(), name='add-chat'),
]
