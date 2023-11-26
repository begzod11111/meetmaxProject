from accounts.models import Profile
from django import template

from article.models import Article
from chats.models import Chat

register = template.Library()


@register.filter(name='check_profile_followers')
def check_profile_followers(profile, request):
	my_profile = request.user.profile.pk
	res = profile.followers.filter(id=my_profile).exists()
	if res:
		return True
	return False


@register.filter(name='check_liked')
def check_liked(obj, user):
	if user.profile in obj.rating.all():
		return True
	return False


@register.filter(name='get_companion_user')
def func(chat, user):
	return chat.members.exclude(user__id=user.id)[0]


@register.filter(name='get_class_message')
def func(message_author_id, user_id):
	if message_author_id == user_id:
		return 'my-message'
	return 'message-me'


@register.filter(name='get_new_messages')
def func(chat, user):
	return len(chat.messages.filter(is_readed=False).exclude(author__user=user))