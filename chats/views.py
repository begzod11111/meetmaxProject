from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, F, OuterRef, Subquery
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView
from .forms import ChatForm
from accounts.models import Profile
from chats.models import Chat, Message


# Create your views here.

class DialogsUserView(TemplateView):
	template_name = 'chats/chat.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.select_related('profile').only(
			'profile__avatar',
			'profile__slug',
			'username',
		).get(id=self.request.user.id)
		if context.get('companion_slug'):
			try:
				context['dialog'] = Chat.objects.prefetch_related(
					Prefetch('members', queryset=Profile.objects.select_related('user').only(
							'pk',
							'user__username',
							'avatar',
						).exclude(user=context['user'])
					),
					Prefetch(
						'messages',
						queryset=Message.objects.select_related('author').only(
							'id',
							'author__slug',
							'author__avatar',
							'message',

						).all().order_by('pub_date')
					)
				).get(
					name=context['companion_slug'],
					type_chat="DCH",
					members=context['user'].profile,
				)
			except Chat.DoesNotExist:
				print('error')
		chats = Message.objects.filter(chat__id=OuterRef('pk')).order_by('-pub_date')
		context['dialogs_list'] = Chat.objects.prefetch_related(
			Prefetch(
				'members', queryset=Profile.objects.select_related('user').only(
					'avatar',
					'user__username'
				).exclude(user=context['user'])
			),
			Prefetch('messages', queryset=Message.objects.only(
				'pk'
			).filter(
				is_readed=False).exclude(author__user=context['user']))
		).only(
			'name',
			'type_chat',
		).annotate(
			last_message=Subquery(chats.values('message'))
		).filter(type_chat='DCH', members=context['user'].profile)
		context['chat_form'] = ChatForm()
		return context


# Message.objects.filter(
# 				group_id=F('pk'),
# 				is_readed=False
# 			).exclude(author=context['user'].profile).count()

