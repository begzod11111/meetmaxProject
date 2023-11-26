from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from utils.managers import MediaPath

from accounts.models import Profile


class Message(models.Model):
    author = models.ForeignKey(Profile, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    message = models.TextField(verbose_name="Сообщение")
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.message


class Chat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to=MediaPath('chat_ava').directory_path_datatime, blank=True)
    admins = models.ManyToManyField(Profile, verbose_name="Администраторы", related_name='admin_chats', blank=True)
    members = models.ManyToManyField(Profile, verbose_name="Участник", related_name='member_chats')
    messages = models.ManyToManyField(Message, verbose_name='Сообщения', related_name='chat', blank=True)

    class Type(models.TextChoices):
        GROUP_CHAT = 'GCH', _('Group Chat')
        DIALOG_CHAT = 'DCH', _('Dialog Chat')
        CHANNEL = 'CH', _('Channel')

    type_chat = models.CharField(max_length=3, choices=Type.choices, default=Type.DIALOG_CHAT)

    @cached_property
    def get_absolute_url(self):
        return reverse('chats:personal_chat_dialog', kwargs={'companion_slug': self.name})

    def __str__(self):
        return f'{self.type_chat}-{self.id}'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_companion_user(self):
        if self.type_chat == 'DCH':
            return self.members.all()[0]


