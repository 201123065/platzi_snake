from django.conf.urls import include, url

from .views  import juego


urlpatterns = [
	url(r'^$',juego.as_view(),name='juego'),
]


