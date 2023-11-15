from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import Profile


class Message(models.Model):

    author = models.ForeignKey(Profile, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    message = models.TextField(verbose_name="Сообщение")
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField('Прочитано', default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message


class GroupChat(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(Profile, verbose_name="Участник", related_name='member_chats')
    admins = models.ManyToManyField(Profile, verbose_name="Администратор", related_name='admin_group_chats')
    messages = GenericRelation(Message)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return f'{self}-{self.id}'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class PrivateChat(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='private_chats')
    user_2 = models.ForeignKey(Profile, on_delete=models.CASCADE)
    messages = GenericRelation(Message)

    @staticmethod
    def get_absolute_url_for_slug(slug):
        return reverse('chats:personal_chat_dialog', kwargs={'companion_slug': slug})

