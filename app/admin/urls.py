from django.conf.urls import url

from app.admin import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.AdminIndexView, name='admin_index'),
    url(r'^/login$', views.AdminLoginView, name='admin_login'),
    url(r'^/logout$', views.logout_admin, name='admin_logout'),
    url(r'^/profile/(?P<username>[\w-]+)$', views.logout_admin, name='admin_detail_profile'),
    url(r'^/csv$', views.some_view, name='some_view'),

    ##########################################################
    ##########################################################
    # User
    url(r'^/user$', views.AdminUserIndexView, name='admin_user_index'),
    url(r'^/user/create$', views.AdminUserCreateView, name='admin_user_create'),
    url(r'^/user/detail/(?P<username>[\w-]+)$', views.AdminUserDetailView, name='admin_user_detail'),
    url(r'^/user/update/(?P<username>[\w-]+)$', views.AdminUserUpdateView, name='admin_user_update'),
    url(r'^/user/update/(?P<username>[\w-]+)/skill$', views.AdminUserEditSkillView, name='admin_user_edit_skill'),
    url(r'^/user/add/skill$', views.add_skill_user, name='admin_user_add_skill'),
    url(r'^/user/delete$', views.admin_user_delete, name='admin_user_delete'),

    ##########################################################
    ##########################################################
    # Team
    url(r'^/team$', views.AdminTeamIndexView, name='admin_team_index'),
    url(r'^/team/create$', views.AdminTeamCreateView, name='admin_team_create'),
    url(r'^/team/detail/(?P<slug>[\w-]+)$', views.AdminTeamDetailView, name='admin_team_detail'),
    url(r'^/team/edit/(?P<slug>[\w-]+)$', views.AdminTeamEditView, name='admin_team_edit'),
    url(r'^/team/edit/(?P<slug>[\w-]+)/skill$', views.AdminTeamEditSkillView, name='admin_team_edit_skill'),
    url(r'^/team/add/skill$', views.add_skill_team, name='admin_team_add_skill'),
    url(r'^/team/delete$', views.admin_team_delete, name='admin_team_delete'),

    ##########################################################
    ##########################################################
    # Project
    url(r'^/project$', views.AdminProjectIndexView, name='admin_project_index'),
    url(r'^/project/create$', views.AdminProjectCreateView, name='admin_project_create'),
    url(r'^/project/detail/(?P<slug>[\w-]+)$', views.AdminProjectDetailView, name='admin_project_detail'),
    url(r'^/project/edit/(?P<slug>[\w-]+)$', views.AdminProjectEditView, name='admin_project_edit'),
    url(r'^/project/edit/(?P<slug>[\w-]+)/team$', views.AdminProjectEditTeamView, name='admin_project_edit_team'),
    url(r'^/project/add_team$', views.add_team_project, name='admin_project_add_team'),
    url(r'^/project/remover_team$', views.remover_team_project, name='admin_project_remover_team'),
    url(r'^/project/delete$', views.admin_project_delete, name='admin_project_delete'),

    ##########################################################
    ##########################################################
    # Skill
    url(r'^/skill$', views.AdminSkillIndexView, name='admin_skill_index'),
    url(r'^/skill/create$', views.AdminSkillCreateView, name='admin_skill_create'),
    url(r'^/skill/detail/(?P<slug>[\w-]+)$', views.AdminSkillDetailView, name='admin_skill_detail'),
    url(r'^/skill/edit/(?P<slug>[\w-]+)$', views.AdminSkillEditView, name='admin_skill_edit'),
    url(r'^/skill/delete$', views.admin_skill_delete, name='admin_skill_delete'),

    ##########################################################
    ##########################################################
    # Position
    url(r'^/position$', views.AdminPositionIndexView, name='admin_position_index'),
    url(r'^/position/create$', views.AdminPositionCreateView, name='admin_position_create'),
    # url(r'^/position/detail/(?P<slug>[\w-]+)$', views.AdminPositionDetailView, name='admin_position_detail'),
    url(r'^/position/edit/(?P<slug>[\w-]+)$', views.AdminPositionEditView, name='admin_position_edit'),
    url(r'^/position/delete$', views.admin_delete_position, name='admin_position_delete'),

    url(r'^/export/$', views.ProfileExport.as_view(), name='country_export'),

    # import
    url(r'^/import/$', views.ProfileImport.as_view(), name='country_import'),
    url(r'^/process_import/$', views.ProfileProcessImport.as_view(), name='process_import'),
]
