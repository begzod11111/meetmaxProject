from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Prefetch

from accounts.models import Profile
from comment.models import Comment
from autoslug import AutoSlugField
# Create your models here.


class PostOptimizationManager(models.Manager):
    def get_queryset(self):
        type_ = ContentType.objects.get_for_model(self.model)
        return super().get_queryset().all().select_related('author__user').only(
            'id',
            'descriptions',
            'file',
            'author__user__username',
            'author__avatar',
            'author__slug',
            'publish_date',
            'media',
        ).prefetch_related(
            Prefetch('comments',
                     queryset=Comment.objects.filter(content_type=type_).select_related('user__profile').only(
                         'object_id',
                         'content_type_id',
                         'id',
                         'content',
                         'user__username',
                         'user__profile__avatar',
                         'count_likes',
                     )),
            Prefetch('likes',
                     queryset=User.objects.all().select_related('profile').only('username',
                                                                                'profile__avatar'))
        ).all()


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='posts')
    publish_date = models.DateField(auto_now=True)
    descriptions = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='posts/files/', blank=True)
    media = models.ImageField(upload_to='posts/media/', blank=True)
    comments = GenericRelation(Comment)
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
    objects = models.Manager()
    optimization_objects = PostOptimizationManager()

    def __str__(self):
        return f'{self.author}-{self.publish_date}'

    def get_comments(self):
        content_type = ContentType.objects.get_for_model(self)
        comments = Comment.objects.select_related('user').filter(content_type=content_type, object_id=self.id)

        return comments

    class Meta:
        ordering = ('-publish_date',)







