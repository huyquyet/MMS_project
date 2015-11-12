from django.conf.urls import url

from app.user import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [
    url(r'^$', views.userindex, name='user_index'),
    url(r'^user/login$', views.UserLoginView, name='user_login'),
    url(r'^user/logout$', views.user_logout, name='user_logout'),
    url(r'^user/edit_profile/(?P<pk>[0-9]+)$', views.UserEditProfileView, name='user_edit_profile'),
    url(r'^user/change_password/(?P<pk>[0-9]+)/$', views.UserChangePassView, name='user_change_pass'),

    url(r'^member$', views.UserMemberIndexView, name='user_member'),
    url(r'^member/detail/(?P<pk>[0-9]+)$', views.UserMemberDetailView, name='user_detail'),
]
