from django.urls import path
from .views import *

app_name = 'article'

urlpatterns = [
	path('all/', ListArticleView.as_view(), name='article_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
	path('<slug:article_slug>/liked/', AddLikeView.as_view(), name='article_like')
]

