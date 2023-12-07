import datetime

import django.utils.timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import strftime
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


def get_path(instance, filename):
    now = timezone.now()
    url = f'{instance._meta.model_name}/%Y/%m/%d/{instance.name}/{filename}'
    return strftime(now, url)


class Chat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to=get_path, blank=True)
    members = models.ManyToManyField(
        Profile,
        through='Membership',
        related_name='chats_member',
        through_fields=("chat", "profile"),
        blank=True
    )
    messages = models.ManyToManyField(Message, verbose_name='Сообщения', related_name='chat', blank=True)

    class Type(models.TextChoices):
        GROUP_CHAT = 'GCH', _('Group Chat')
        DIALOG_CHAT = 'DCH', _('Dialog Chat')
        CHANNEL = 'CH', _('Channel')

    type_chat = models.CharField(max_length=3, choices=Type.choices, default=Type.DIALOG_CHAT)

    @cached_property
    def get_absolute_url(self):
        return reverse('chats:personal_chat_dialog', kwargs={
            'companion_slug': self.name,
            'type_chats': self.get_type_chat(self.type_chat)
        })

    @staticmethod
    def get_type_chat(type_chats):
        available_slugs = {
            'dialogues': 'DCH', 'groups': 'GCH', 'channels': 'CH'
        }
        for key, val in available_slugs.items():
            if type_chats == key:
                return val
            elif type_chats == val:
                return key
        raise Http404

    def __str__(self):
        return f'{self.type_chat}-{self.id}'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_companion_user(self):
        if self.type_chat == 'DCH':
            return self.members.all()[0]

    def members_add(self, profile, is_admin=False, is_author=False):
        date = timezone.now()
        self.members.add(profile, through_defaults={
            'is_admin': is_admin,
            'is_author': is_author,
            'date_joined': date,
        })

    @classmethod
    def has_chat(cls, chat_name: str, type_chat: str):
        if len(type_chat) > 3:
            type_chat = cls.get_type_chat(type_chat)
        try:
            chat = cls.objects.get(
                name=chat_name,
                type_chat=type_chat
            )
            return chat
        except cls.DoesNotExist:
            return False

    @staticmethod
    def generic_name(profile_1: Profile, profile_2: Profile) -> str:
        if profile_1.id > profile_2.id:
            name = str(profile_1.user.username + '_' + profile_2.user.username)
        else:
            name = str(profile_2.user.username + '_' + profile_1.user.username)
        return name
    
    def delete(self, using=None, keep_parents=False):
        self.messages.all().delete()
        super().delete()


class Membership(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='memberships')
    is_admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False, null=True)
    is_author = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "chats_chat_members"



