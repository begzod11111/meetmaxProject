from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils.mixins import JsonView
from post.models import Post
from .forms import *


# Create your views here.


class AddComment(JsonView):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST.get('post_id'))
        comment = Comment(content_object=post, content=request.POST.get('comment_text'), user=request.user)
        comment.count_likes = 0
        comment.save()
        if comment.pk:
            data = {
                'comment_id': comment.pk,
                'status': True,
                'ava_user': comment.user.profile.avatar.url,
                'username': comment.user.username,
                'comment_text': comment.content,
            }
            return self.render_to_response(data)


class AddLikeCommentView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = Comment.objects.only('pk').get(id=request.POST['comment_id'])
            content_type = ContentType.objects.get_for_model(comment)
            like_or_dislike = True if request.POST['like_or_dislike'] == 'like' else False
            try:
                like = Like.objects.only('like_or_dislike').get(
                    content_type=content_type, object_id=comment.pk,
                    user__id=request.user.id)
                if like.like_or_dislike == like_or_dislike:
                    like.delete()
                    return JsonResponse({
                        'status': True,
                        'count': comment.get_count_rating()
                    })

            except Like.DoesNotExist:
                like = Like(content_object=comment, user=request.user, like_or_dislike=like_or_dislike)
                like.save()
                if like.pk:
                    return JsonResponse({
                        'status': True,
                        'count': comment.get_count_rating()
                        })
        return HttpResponse('error')





