from django.conf.urls import url

from app.admin import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.AdminIndexView, name='admin_index'),
    url(r'^/login$', views.AdminLoginView, name='admin_login'),
    url(r'^/logout$', views.logout_admin, name='admin_logout'),
    url(r'^/profile/(?P<username>[\w-]+)$', views.logout_admin, name='admin_detail_profile'),

    ##########################################################
    ##########################################################
    # User
    url(r'^/user$', views.AdminUserIndexView, name='admin_user_index'),
    url(r'^/user/create$', views.AdminUserCreateView, name='admin_user_create'),
    url(r'^/user/detail/(?P<username>[\w-]+)$', views.AdminUserDetailView, name='admin_user_detail'),
    url(r'^/user/update/(?P<username>[\w-]+)$', views.AdminUserUpdateView, name='admin_user_update'),
    url(r'^/user/update/(?P<username>[\w-]+)/skill$', views.AdminUserEditSkillView, name='admin_user_edit_skill'),
    url(r'^/user/add/skill$', views.add_skill_user, name='admin_user_add_skill'),

    ##########################################################
    ##########################################################
    # Team
    url(r'^/team$', views.AdminTeamIndexView, name='admin_team_index'),
    url(r'^/team/create$', views.AdminTeamCreateView, name='admin_team_create'),
    url(r'^/team/detail/(?P<slug>[\w-]+)$', views.AdminTeamDetailView, name='admin_team_detail'),
    url(r'^/team/edit/(?P<slug>[\w-]+)$', views.AdminTeamEditView, name='admin_team_edit'),
    url(r'^/team/edit/(?P<slug>[\w-]+)/skill$', views.AdminTeamEditSkillView, name='admin_team_edit_skill'),
    url(r'^/team/add/skill$', views.add_skill_team, name='admin_team_add_skill'),

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
    url(r'^/skill/detail/(?P<slug>[\w-]+)$', views.AdminSkillDetailView, name='admin_skill_detail'),
    url(r'^/skill/edit/(?P<slug>[\w-]+)$', views.AdminSkillEditView, name='admin_skill_edit'),

    ##########################################################
    ##########################################################
    # Position
    url(r'^/position$', views.AdminPositionIndexView, name='admin_position_index'),
    url(r'^/position/create$', views.AdminPositionCreateView, name='admin_position_create'),
    # url(r'^/position/detail/(?P<slug>[\w-]+)$', views.AdminPositionDetailView, name='admin_position_detail'),
    url(r'^/position/edit/(?P<slug>[\w-]+)$', views.AdminPositionEditView, name='admin_position_edit'),
]
