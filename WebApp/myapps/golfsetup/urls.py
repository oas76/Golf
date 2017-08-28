from django.conf.urls import url

from . import views

app_name = 'golfsetup'
urlpatterns = [
    # ex: /golfsetup/
    url(r'^$', views.index, name='index'),
    # ex: /golfsetup/player/5/
    url(r'^players/$', views.players, name='players'),
    # ex: /golfsetup/player/5/
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player, name='player'),
    # ex: /golfsetup/tournamnet/1/
    url(r'tournament/(?P<tournament_id>[0-9]+)/$', views.tournament, name='tournament'),
]