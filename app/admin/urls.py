from django.conf.urls import url

from app.admin import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.AdminIndexView, name='admin_index'),
    url(r'^/login$', views.AdminLoginView, name='admin_login'),
    url(r'^/logout$', views.logout_admin, name='admin_logout'),
    url(r'^/profile/(?P<username>[\w-])$', views.logout_admin, name='admin_detail_profile'),

    ##########################################################
    ##########################################################
    # Team
    url(r'^/team$', views.AdminTeamIndexView, name='admin_team_index'),
    url(r'^/team/create$', views.AdminTeamCreateView, name='admin_team_create'),

    ##########################################################
    ##########################################################
    # Project
    url(r'^/project$', views.AdminProjectIndexView, name='admin_project_index'),
    url(r'^/project/create$', views.AdminProjectCreateView, name='admin_project_create'),

    ##########################################################
    ##########################################################
    # Skill
    url(r'^/skill$', views.AdminSkillIndexView, name='admin_skill_index'),
    url(r'^/skill/create$', views.AdminSkillCreateView, name='admin_skill_create'),
]
