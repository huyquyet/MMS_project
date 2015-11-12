from django.conf.urls import url
from app.skill import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [
    url(r'^$', views.SkillIndexView, name='skill_index'),
]
