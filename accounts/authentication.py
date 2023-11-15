import requests
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from social_core.pipeline.user import create_user
from django.shortcuts import redirect
from social_core.backends.google import GoogleOAuth2


class EmailAuthBackend:

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class AuthenticationGoogleView(GoogleOAuth2):

    def get_user_id(self, details, response):
        id_ = super().get_user_id(details, response)
        return id_

    def get_user(self, user_id):
        user = super().get_user(user_id)
        return user

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        data = self.get_json(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": "Bearer %s" % access_token,
            },
        )
        return data

    def do_auth(self, access_token, *args, **kwargs):
        user = super().do_auth(access_token, *args, **kwargs)
        return user

