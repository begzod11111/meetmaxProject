import json

from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, F, OuterRef, Subquery, Count
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from accounts.mixins import BaseContextDataMixin
from .forms import ChatForm
from accounts.models import Profile
from chats.models import Chat, Message, Membership


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
		context['type_chats'] = Chat.get_type_chat(context['type_chats'])
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
					members=context['user'].profile,
				)
			except Chat.DoesNotExist:
				raise Http404('Чат не найдено')
		chats = Message.objects.filter(chat__id=OuterRef('pk')).order_by('-pub_date')
		context['dialogs_list'] = Chat.objects.prefetch_related(
			Prefetch(
				'members', queryset=Profile.objects.select_related('user').only(
					'avatar',
					'user__username'
				).exclude(user=context['user'])
			)
		).only(
			'name',
			'avatar',
			'type_chat',
		).annotate(
			last_message=Subquery(chats.values('message')),
			notreaded_message_count=Count(
				'messages', filter=Q(messages__is_readed=False) & ~Q(messages__author=context['user'].profile)
			)
		).filter(type_chat=context['type_chats'], members=context['user'].profile)
		context['members'] = Profile.objects.select_related('user').only(
			'user__username',
			'user__last_name',
			'user__first_name',
			'avatar'
		).filter(
			Q(following=context['user'].profile) & Q(followers=context['user'].profile)
		)
		context['chat_form'] = ChatForm()
		return context


class AddDCHView(BaseContextDataMixin, View):
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		user_profile = Profile.objects.get(id=request.POST.get('user_id'))
		chat_name = Chat.generic_name(request.user.profile, user_profile)
		chat = Chat.has_chat(chat_name=chat_name, type_chat="DCH")
		if not chat:
			chat = Chat.objects.create(
				type_chat="DCH",
				name=chat_name,
			)
			chat.members_add(user_profile)
			chat.members_add(request.user.profile, is_author=True)
		return JsonResponse({
			'satus': True,
			'path': chat.get_absolute_url
		})


class AddChatView(View):

	def post(self, request):
		form = ChatForm(request.POST, request.FILES)
		print(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			obj.members_add(request.user.profile, is_author=True)
			return JsonResponse({
				'path': obj.get_absolute_url
			})
		return HttpResponse('error')


class CheckOnlineUser(View):
	def get(self, request):
		companion_username = request.GET.get('companion_username')
		room_name = request.GET.get('room_name')
		user_profile = Profile.objects.get(user__username=companion_username)
		res = user_profile.memberships.get(chat__name=room_name)
		if res.is_online:
			return JsonResponse({
				'status': True
			})
		data = {
			'status': False,
			'last_activity': res.last_activity.isoformat()
		}
		json_data = json.dumps(data)
		return JsonResponse(json_data, safe=False)


