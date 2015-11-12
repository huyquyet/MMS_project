from django.conf.urls import url
from app.project import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.ProjectIndexView, name='project_index'),
]