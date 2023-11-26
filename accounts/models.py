import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import ValuesIterable
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.datetime_safe import strftime
from django.utils.functional import cached_property
from django.utils.text import slugify
from utils.managers import MediaPath

# Create your models here.


# class UpdateManager(models.Manager):
#
#     def values(self, *fields, **expressions):
#         fields += tuple(expressions)
#         print(fields)
#         clone = self._values(*fields, **expressions)
#         print(clone)
#         clone._iterable_class = ValuesIterable
#         print(clone)
#         return clone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(unique=True)
    avatar = models.ImageField(
        upload_to=MediaPath('avatars').directory_path_datatime,
        blank=True,
        default="default/avatars/avatar_default.png",
        verbose_name='Фото профиля'
        )
    bio = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(blank=True, null=True)
    banner = models.ImageField(upload_to=MediaPath('banner').directory_path_datatime,
                               blank=True,
                               default='default/banners/banner_default.jpg')
    instagram = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    website = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    following = models.ManyToManyField('Profile', blank=True, related_name='followers')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    @cached_property
    def get_absolute_url_profile(self):
        return reverse('accounts:user-profile', kwargs={"user_slug": self.slug})

    @cached_property
    def get_absolute_url_settings(self):
        return reverse('accounts:user-settings', kwargs={'user_slug': self.slug})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            pro = Profile(user=instance)
            pro.slug = slugify(instance.username)
            pro.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_followers(self):
        followers = self.followers.all()
        return followers

    def get_following(self):
        following = self.following.all()
        return following

    def get_followers_count(self):
        count = self.followers.count()
        return count

    def get_following_count(self):
        count = self.following.count()
        return count

    def get_files_name(self):
        names = {
            'avatar': self.avatar.name.split('/')[-1].split('.')[0],
            'banner': self.banner.name.split('/')[-1].split('.')[0]
        }
        return names




