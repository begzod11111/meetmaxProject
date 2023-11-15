from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, F
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.models import Profile
from chats.models import PrivateChat


# Create your views here.


def test(request):
	return render(request, 'chats/chat.html')


class DialogsUserView(TemplateView):
	template_name = 'chats/chat.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.select_related('profile').only(
			'profile__avatar',
			'profile__slug',
			'username'
		).get(id=self.request.user.id)
		if context.get('companion_slug'):
			context['dialog'] = PrivateChat.objects.get(
				Q(author__user=context['user']), Q(user_2__slug=context['companion_slug'])
			)
		context['dialogs_list'] = PrivateChat.objects.select_related('user_2__user').only(
			'user_2__avatar',
			'user_2__slug',
			'user_2__user__username',

		).annotate(
			absolute_url=F('user_2__slug')
		).filter(Q(author__user=context['user']))
		for i in context['dialogs_list']:
			i.absolute_url = i.get_absolute_url_for_slug(i.absolute_url)
		return context
