from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('add-comment/', AddComment.as_view(), name='add_comment'),
    path('like-comment/', AddLikeCommentView.as_view(), name='add_rating_for_comment')
]
