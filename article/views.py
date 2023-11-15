from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import ContextMixin

from accounts.models import Profile
from article.models import Article, Tag
from comment.models import Comment
from utils.mixins import JsonView


# Create your views here.


class ListArticleView(TemplateView):
	template_name = 'article/explore.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['user'] = User.objects.only(
				'profile__avatar',
				'profile__slug',
				'username'
			).select_related('profile').get(id=self.request.user.id)
		context['articles'] = Article.objects.prefetch_related(
			Prefetch('tags', queryset=Tag.objects.only('name').all())
		).all()
		return context


class ArticleDetailView(TemplateView):
	template_name = 'article/article-detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if self.request.user.is_authenticated:
			context['user'] = User.objects.only(
				'profile__avatar',
				'profile__slug',
				'username'
			).select_related('profile').get(id=self.request.user.id)
		context['object'] = Article.objects.select_related('auther__profile').prefetch_related(
			Prefetch('comments', queryset=Comment.objects.select_related('user__profile').only(
				'user__username',
				'user__profile__avatar',
				'publish_date',
				'content',
				'content_type_id',
				'object_id'
			).all()),
			Prefetch('rating', queryset=Profile.objects.only('pk').all())

		).only(
			'slug',
			'auther__username',
			'publish_date',
			'auther__profile__avatar',
			'banner',
			'text',
			'title',

		).get(
			publish_date__year=context['year'],
			publish_date__month=context['month'],
			publish_date__day=context['day'],
			slug=context['article_slug']
		)

		return context


class AddLikeView(View, ContextMixin):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		del context['view']
		context['article'] = Article.objects.get(slug=context['article_slug'])

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		profile = request.user.profile
		if context['article'].rating.filter(slug=profile.slug).exists():
			context['article'].rating.remove(profile)
			return JsonResponse({
				'flag': False
			})
		context['article'].rating.add(profile)
		return JsonResponse({
			'flag': True
		})


class AddCommentArticle(JsonView):
	pass
