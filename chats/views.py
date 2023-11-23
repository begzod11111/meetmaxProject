from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, F
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

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
			context['dialog'] = Chat.objects.prefetch_related(
				Prefetch('members', queryset=Profile.objects.only(
						'pk',
						'avatar',
					).all()
				),
				Prefetch(
					'messages',
					queryset=Message.objects.select_related('author', 'group').only(
						'id',
						'author__slug',
						'author__avatar',
						'message',
						'group_id'

					).all()
				)
			).get(
				name=context['companion_slug'],
				type_chat="DCH",
				members=context['user'].profile,
			)
		context['dialogs_list'] = Chat.objects.prefetch_related(
			Prefetch(
				'members', queryset=Profile.objects.select_related('user').only(
					'avatar',
					'user__username'
				).exclude(user=context['user'])
			)
		).only(
			'name',
		).filter(type_chat='DCH')
		return context
