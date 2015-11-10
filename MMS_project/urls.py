"""MMS_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from MMS_project import settings

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),
    url(r'^admin', include('app.admin.urls', namespace='admin')),
    url(r'^', include('app.user.urls', namespace='user')),
    url(r'^position', include('app.position.urls', namespace='position')),
    url(r'^project', include('app.project.urls', namespace='project')),
    url(r'^team', include('app.team.urls', namespace='team')),
    url(r'^skill', include('app.skill.urls', namespace='skill')),
]
