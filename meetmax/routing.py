from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter

import chats.routing

application = ProtocolTypeRouter({
	'wedsocket': AuthMiddlewareStack(
		URLRouter(chats.routing.wedsocket_urlpatterns)
	),
})
