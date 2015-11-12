from django.conf.urls import url

from app.team import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.TeamIndexView, name='team_index'),
    url(r'^/detail/(?P<slug>[\w-]+)$', views.TeamDetailView, name='team_detail'),
]
