from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin, BaseDeleteView

from accounts.models import Profile
from comment.models import Comment
from rating.models import Like
from .forms import PostForm
from .models import Post
from accounts.mixins import BaseContextDataMixin
from utils.mixins import JSONResponseMixin

# Create your views here.


class PostsView(TemplateView):
    template_name = 'post/posts.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form_post'] = PostForm

        context["all_posts"] = Post.optimization_objects.all()
        if request.user.is_authenticated:
            context['user'] = User.objects.select_related('profile').only(
                'profile__slug',
                'profile__avatar',
                'username',
                'pk',
                ).get(id=request.user.id)
        return self.render_to_response(context)


class AddPost(View):

    def post(self, request):
        user = request.user.profile
        data = request.POST.copy()
        data['author'] = user.pk
        if data.get("descriptions") or request.FILES.get('media') or request.FILES.get("file"):
            form = PostForm(data, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')
            return HttpResponse('lose')
        return HttpResponse('error')


class DeletePost(SingleObjectMixin, DeletionMixin, View):
    pk_url_kwarg = 'post_id'
    model = Post
    object = None
    success_url = reverse_lazy('posts_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AddLikeView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        post = Post.objects.get(id=request.POST['post_id'])
        data['liked'] = True
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
            data['liked'] = False
        post.save()
        data['count_likes'] = post.likes.count()

        return JsonResponse(data)


