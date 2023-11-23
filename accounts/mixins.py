from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View, TemplateView


class BaseContextDataMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug = context.get('user_slug')
		if slug:
			try:
				context['user'] = User.objects.select_related('profile').only(
					'profile__slug',
					'profile__avatar',
					'profile__banner',
					'username',
					'profile__bio'
				).get(profile__slug=slug)
			except User.DoesNotExist:
				raise Http404
		return context


class BaseGetUserMixin(ContextMixin):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['current_user'] = User.objects.select_related('profile').only(
				'profile__slug',
				'profile__avatar',
				'profile__banner',
				'username',
				'profile__bio'
			).get(id=self.request.user.id)
		except User.DoesNotExist:
			raise Http404

		return context


class BaseSingInMixin(LoginRequiredMixin):
	redirect_field_name = ''
	login_url = reverse_lazy('accounts:sing_in')
