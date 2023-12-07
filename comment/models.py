from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count, Q
from django.utils.functional import cached_property

from utils.managers import MediaPath
from rating.models import Like

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)
    media_files = models.FileField(upload_to=MediaPath('media_files').directory_path_datatime, null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    count_likes = models.IntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation(Like)

    def __str__(self):
        return f'{self.user}-{self.content[:20]}'

    class Meta:
        ordering = ['-count_likes', '-publish_date']
    @classmethod
    def get_comment_rating(cls, comment_id):
        comment = cls.objects.annotate(
            comment_rating=(Count('likes', filter=Q(likes__like_or_dislike=True)) -
                            Count('likes', filter=Q(likes__like_or_dislike=False)))
        ).only('pk', 'count_likes').get(id=comment_id)
        comment.count_likes = comment.comment_rating
        comment.save()
        return comment

