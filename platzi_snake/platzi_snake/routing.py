from channels import include

channel_routing = [
	include("snake_protocol.routing.websocket_routing",path=r'^/ws_platzi'),
]

