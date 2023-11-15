from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse

from accounts.models import Profile
from comment.models import Comment
from rating.models import Like


# Create your models here.


class Article(models.Model):
	auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	banner = models.ImageField(upload_to='article/banners', blank=True)
	title = models.CharField(max_length=300, unique=True)
	slug = AutoSlugField(populate_from='title', unique=True)
	publish_date = models.DateField(auto_now=True)
	text = models.TextField()
	tags = models.ManyToManyField('Tag', blank=True, related_name='articles')
	comments = GenericRelation(Comment, blank=True)
	rating = models.ManyToManyField(Profile, blank=True)

	def get_absolute_url(self):
		return reverse('article:article_detail', kwargs={
			'year': self.publish_date.year,
			'month': self.publish_date.month,
			'day': self.publish_date.day,
			'article_slug': self.slug,
		})

	def get_comments(self):
		content_type = ContentType.objects.get_for_model(self)
		comments = Comment.objects.filter(content_type=content_type, object_id=self.id)

		return comments

	def __str__(self):
		return f'{self.auther}-{self.id}'


class Tag(models.Model):
	name = models.CharField(max_length=200)
	slug = AutoSlugField(populate_from='name')

	def __str__(self):
		return self.name
