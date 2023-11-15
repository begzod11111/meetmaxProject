from django.urls import path
from .views import *
from accounts.views import *

urlpatterns = [
    path('', PostsView.as_view(), name='posts_list'),
    path('add-post/', AddPost.as_view(), name='add_post'),
    path('<int:post_id>/delete/', DeletePost.as_view(), name='delete_post'),
    path('like/', AddLikeView.as_view(), name='add_like_post')
]
