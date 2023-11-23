import os

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Prefetch, Count
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateResponseMixin, TemplateView, ContextMixin
from django.views.generic.edit import BaseFormView
from post.forms import PostForm
from post.models import Post
from .forms import *
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from .mixins import BaseContextDataMixin, BaseSingInMixin
from utils.mixins import JsonView


# Create your views here.


class CreateUser(CreateView):
	model = User
	form_class = RegistrationUserForm
	template_name = 'accounts/sing_up.html'
	context_object_name = 'form'
	success_url = reverse_lazy('accounts:sing_in')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


class CheckUsername(JsonView):
	def get(self, request, *args, **kwargs):
		username = request.GET.get('username', None)
		data = {
			'is_taken': User.objects.filter(username=username).exists()
		}
		print(reverse('accounts:password-reset'))
		return JsonResponse(data)


class LoginUserView(LoginView):
	template_name = 'accounts/sing_in.html'

	def get_success_url(self):
		user = self.request.user
		return reverse_lazy('accounts:user-profile', kwargs={'user_slug': user.profile.slug})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['password_reset_form'] = PasswordResetForm()
		return context


def logout_user(request):
	logout(request)
	return redirect('posts_list')


class UserProfileView(BaseSingInMixin, TemplateView):
	template_name = 'accounts/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['user'] = User.objects.select_related('profile').annotate(
				following=Count('profile__following'),
				followers=Count('profile__followers')
			).get(id=self.request.user.id)
		except User.DoesNotExist:
			raise Http404

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		slug = context.get('user_slug')
		if context['user'].profile.slug != slug:
			context['current_user'] = User.objects.select_related('profile').annotate(
				following=Count('profile__following'),
				followers=Count('profile__followers')
			).get(profile__slug=slug)
			context['guest'] = True
			context['user_posts'] = Post.optimization_objects.filter(author=context['current_user'].profile)
		else:
			context['current_user'] = context['user']
			context['form_post'] = PostForm
			context['guest'] = False
			context['user_posts'] = Post.optimization_objects.filter(author=context['user'].profile)
		return self.render_to_response(context)


class UserSettingsView(BaseSingInMixin, TemplateResponseMixin, ContextMixin, View):
	template_name = 'accounts/user_settings.html'

	def get(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.select_related('profile').get(profile__slug=context['user_slug'])
		context['user_profile_form'] = ProfileUserForm(instance=user.profile)
		context['user_form'] = UserForm(instance=user)
		context['change_password_form'] = PasswordChangeForm(user=user)
		context['user'] = user
		return self.render_to_response(context)


class UserUpdateView(View, BaseContextDataMixin):

	def post(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		form = UserForm(request.POST, instance=context['user'])
		profile_form = ProfileUserForm(request.POST, request.FILES, instance=context['user'].profile)
		if request.FILES.get('avatar'):
			url = context['user'].profile.avatar.path
			if context['user'].profile.get_files_name()['avatar'] != 'avatar_default':
				os.remove(url)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			return redirect(context['user'].profile.get_absolute_url_settings)
		errors = {}
		if form.errors:
			errors.update(form.errors.get_json_data())
		if profile_form.errors:
			errors.update(profile_form.errors.get_json_data())
		for key, val in errors.items():
			for error in val:
				messages.add_message(request, messages.ERROR, f'{key} - {error["message"]}')
		return redirect(context['user'].profile.get_absolute_url_settings)


class UserPasswordChange(BaseFormView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('accounts:sing_in')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


# class UserFollowersView(UserCommunityView):
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		objects = context['user'].profile.get_followers()
# 		context['page'] = Paginator(objects, 12)
# 		context['page_obj'] = context['page'].page(1).object_list
# 		context['nav'] = 2
# 		return context
#
# 	def get(self, request, *args, **kwargs):
# 		context = self.get_context_data(**kwargs)
# 		page_num = request.GET.get('page')
# 		print(context['page'])
# 		if page_num:
# 			data = super().get_json_data(request, context['page'], page_num, check_user=True)
# 			return JsonResponse(data)
# 		return self.render_to_response(context)


# class UserFollowingView(UserCommunityView):
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		objects = context['user'].profile.get_following()
# 		context['page'] = Paginator(objects, 12)
# 		context['page_obj'] = context['page'].page(1).object_list
# 		context['nav'] = 1
#
# 		return context
#
# 	def get(self, request, *args, **kwargs):
# 		context = self.get_context_data(**kwargs)
# 		page_num = request.GET.get('page')
# 		if page_num:
# 			data = super().get_json_data(request, context['page'], page_num, check_user=True)
# 			return JsonResponse(data)
# 		return self.render_to_response(context)


class FollowUser(View, BaseContextDataMixin):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		flag = True
		user = context['user']
		user_follow = Profile.objects.get(slug=request.POST.get('user_slug'))
		if user.profile.following.filter(slug=request.POST.get('user_slug')).exists():
			user.profile.following.remove(user_follow)
			flag = False
		else:
			user.profile.following.add(user_follow)
		data = {
			'flag': flag
		}
		return JsonResponse(data)


class ListCommunityView(BaseSingInMixin, TemplateView):
	available_slugs = ['followers', 'following', 'interesting-profile']
	template_name = 'accounts/my_community.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		method, lookup = None, None
		if context['following_or_followers'] == 'following':
			context['nav'] = 1
			lookup = 'profile__following'
			method = Profile.get_following
		elif context['following_or_followers'] == 'followers':
			context['nav'] = 2
			lookup = 'profile__followers'
			method = Profile.get_followers
		context['user'] = User.objects.select_related('profile').only(
			'username',
			'profile__slug',
			'profile__avatar'
		).prefetch_related(
			Prefetch('profile__following', queryset=Profile.objects.select_related('user').only(
				'user__username',
				'avatar',
				'slug',
				'bio'
			)),
			Prefetch('profile__followers', queryset=Profile.objects.select_related('user').only(
				'user__username',
				'avatar',
				'slug',
				'bio'
			))
		).get(id=self.request.user.id)
		context['objects'] = method(context['user'].profile).order_by('id')
		return context

	def get_json_data(self, user, page, page_num):
		data = {'flag': None}
		try:
			page_obj = page.page(page_num)
			for i in page_obj.object_list:
				data[i.user.username] = {
					'avatar': i.avatar.url,
					'link': None,
					'slug': i.slug,
					'follow': True if i in user.profile.following.all() else False
				}
			data['flag'] = True
			return data
		except EmptyPage:
			data['flag'] = False
			return data

	# @login_required(login_url='/accounts/sing-in/')
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		objects = context['objects']

		context['page'] = Paginator(objects, 12)
		context['page_obj'] = context['page'].page(1).object_list
		page_num = request.GET.get('page')
		if page_num:
			data = self.get_json_data(context['user'], context['page'], page_num)
			return JsonResponse(data)
		return self.render_to_response(context)


class UpdateBannerProfile(View):
	def post(self, request, *args, **kwargs):
		user_profile = Profile.objects.get(slug=kwargs['user_slug'])
		if user_profile.get_files_name()['banner'] != 'banner_default':
			os.remove(user_profile.banner.path)
		user_profile.banner = request.FILES['file']
		user_profile.save()
		return JsonResponse({
			'status': True,
			'path': user_profile.banner.url
		})

