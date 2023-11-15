from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, JsonResponse
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
