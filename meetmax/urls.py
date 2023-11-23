from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls',  namespace='accounts')),
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('comment/', include('comment.urls', namespace='comments')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('article/', include('article.urls', namespace='article')),
    path('chat/', include('chats.urls', namespace='chats')),

]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
