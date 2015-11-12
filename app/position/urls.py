from django.conf.urls import url
from app.position import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'


urlpatterns = [
    url(r'^$', views.PositionIndexView, name='position_index'),
]
