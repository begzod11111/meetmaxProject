from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'chats'

urlpatterns = [
	# path('add-chat/', )
	path('dialog/all/', login_required(DialogsUserView.as_view()), name='dialogs'),
	path('dialog/<str:companion_slug>/', login_required(DialogsUserView.as_view()), name='personal_chat_dialog'),

	# path(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
]
