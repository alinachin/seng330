from django.conf.urls import patterns, include, url
from django.contrib import admin
import player.views

urlpatterns = patterns('',
    url(r'^$', player.views.player_dashboard),
    url(r'^login/$', player.views.login),
    url(r'^logout/$', player.views.player_logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', player.views.register),
    url(r'^accounts/login/$', player.views.login),
    url(r'^new_game/$', player.views.new_game),

)
