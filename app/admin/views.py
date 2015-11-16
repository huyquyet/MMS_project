import tempfile

from django.contrib import auth
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView, UpdateView, View
from import_export.formats import base_formats
from import_export.forms import ImportForm, ConfirmImportForm, os
from import_export.resources import modelresource_factory
from import_export.results import RowResult
from app.admin.forms import TeamCreateFormView, ProjectCreateFormView, SkillCreateFormView, PositionCreateFormView, UserCreateFormView, UserUpdateFormView, TeamEditFormView, CountryResource
from app.position.function import return_list_user_of_position, set_position_list_user
from app.position.models import Position
from app.project.function import return_total_project_of_team, return_list_project_of_team, return_total_team_of_project, return_list_team_of_project, return_list_leader_of_project, \
    return_list_team_not_of_project
from app.project.models import Project, TeamProject
from app.skill.function import return_total_skill_of_team, count_user_of_skill, count_team_of_skill, count_skill_of_user, return_list_skill_of_user, return_list_skill_not_of_user, return_list_skill_of_team, \
    return_list_skill_not_of_team, return_list_user_of_skill, return_list_team_of_skill
from app.skill.models import Skill, UserSkill
from app.team.function import return_total_user_of_team, return_list_member_of_team, return_list_member_leader, return_leader_of_team, set_team_list_user
from app.team.models import Team
from app.user.function import return_team_of_user, return_position_of_user, check_leader
from app.user.models import Profile
from django.http import HttpResponse

requirement_admin = user_passes_test(lambda u: u.is_staff, login_url='admin:admin_login')


class AdminIndex(TemplateView):
    template_name = 'admin/layout/base_admin.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Admin index'
        return super().dispatch(request, *args, **kwargs)


AdminIndexView = AdminIndex.as_view()


class AdminLogin(FormView):
    form_class = AdminAuthenticationForm
    template_name = 'admin/admin_login.html'

    def get_success_url(self):
        link = self.request.POST.get('next', False)
        if link:
            return link
        else:
            return reverse('admin:admin_index')

    def form_valid(self, form):
        user_form = form.get_user()
        login(self.request, user_form)
        return super().form_valid(form)


AdminLoginView = AdminLogin.as_view()


@requirement_admin
def logout_admin(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('admin:admin_index'))


class AdminProfileView(DetailView):
    model = User
    template_name = 'admin/admin_detail_profile.html'
    context_object_name = ''

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Profile Admin'
        return super().dispatch(request, *args, **kwargs)


AdminProfileView = AdminProfileView.as_view()

""" ----------------------------------------------------------------------
    View User Admin
-----------------------------------------------------------------------"""


class AdminUserIndex(ListView):
    model = User
    template_name = 'admin/user/admin_user_index.html'
    paginate_by = 15
    context_object_name = 'list_user'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'User Index'
        return super(AdminUserIndex, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False)

    def get_context_data(self, **kwargs):
        ctx = super(AdminUserIndex, self).get_context_data(**kwargs)
        for user in ctx['list_user']:
            user.team = return_team_of_user(user)
            user.position = return_position_of_user(user)
            user.skill = count_skill_of_user(user)
        return ctx


AdminUserIndexView = AdminUserIndex.as_view()


class AdminUserCreate(CreateView):
    model = User
    template_name = 'admin/user/admin_user_create.html'
    form_class = UserCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Create new user'
        return super(AdminUserCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_team'] = Team.objects.all()
        ctx['list_position'] = Position.objects.all()
        return ctx

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(self.request.POST.get('password'))
        user.save()
        form.save()
        team = self.request.POST.get('team_id')
        position = self.request.POST.get('position_id')
        profile = Profile.objects.create(user=user, team=Team.objects.get(id=team), position=Position.objects.get(id=position))
        profile.save()
        return super(AdminUserCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:admin_user_index')


AdminUserCreateView = AdminUserCreate.as_view()


class AdminUserDetail(DetailView):
    model = User
    template_name = 'admin/user/admin_user_detail.html'
    context_object_name = 'detail_user'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'User detail'
        return super(AdminUserDetail, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['detail_user'].team = return_team_of_user(ctx['detail_user'])
        ctx['detail_user'].position = return_position_of_user(ctx['detail_user'])
        ctx['detail_user'].skill = count_skill_of_user(ctx['detail_user'])
        ctx['list_skill_user'] = return_list_skill_of_user(ctx['detail_user'])
        return ctx


AdminUserDetailView = AdminUserDetail.as_view()


class AdminUserUpdate(UpdateView):
    model = User
    form_class = UserUpdateFormView
    template_name = 'admin/user/admin_user_update.html'
    context_object_name = 'update_user'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'User detail'
        return super(AdminUserUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['update_user'].team = return_team_of_user(ctx['update_user'])
        ctx['update_user'].position = return_position_of_user(ctx['update_user'])
        # ctx['detail_user'].skill = count_skill_of_user(ctx['detail_user'])
        # ctx['list_skill_user'] = return_list_skill_of_user(ctx['detail_user'])
        ctx['list_team'] = Team.objects.all()
        ctx['list_position'] = Position.objects.all()
        return ctx

    def form_valid(self, form):
        user = form.save()
        profile = user.profile
        profile.team = Team.objects.get(id=self.request.POST.get('team_id'))
        profile.position = Position.objects.get(id=self.request.POST.get('position_id'))
        profile.save()
        return super(AdminUserUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:admin_user_index')


AdminUserUpdateView = AdminUserUpdate.as_view()


class AdminUserEditSkill(DetailView):
    model = User
    template_name = 'admin/user/admin_user_edit_skill.html'
    context_object_name = 'detail_user'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'User detail'
        return super(AdminUserEditSkill, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_skill_user'] = return_list_skill_of_user(self.object)
        ctx['list_skill'] = return_list_skill_not_of_user(self.object)
        return ctx


AdminUserEditSkillView = AdminUserEditSkill.as_view()


def add_skill_user(request):
    skill_id = request.POST.get('skill_id', None)
    year = request.POST.get('year', None)
    level = request.POST.get('level', None)
    user = request.POST.get('user', None)
    if user is not None:
        if skill_id is None or year is None or level is None:
            return HttpResponseRedirect(reverse('admin:admin_user_edit_skill', kwargs={'username': user}))
        else:
            skill, create = UserSkill.objects.get_or_create(user=User.objects.get(username=user), skill=Skill.objects.get(id=skill_id), level=level, year=year)
            skill.save()
            return HttpResponseRedirect(reverse('admin:admin_user_edit_skill', kwargs={'username': user}))
    else:
        return HttpResponseRedirect(reverse('admin:admin_user_index'))


def admin_user_delete(request):
    id_user = request.POST.get('id_user', None)
    if id_user is not None:
        user = get_object_or_404(User, pk=id_user)
        if check_leader(user):
            return HttpResponseRedirect(reverse('admin:admin_user_index'))
        else:
            user.delete()
            return HttpResponseRedirect(reverse('admin:admin_user_index'))
    else:
        return HttpResponseRedirect(reverse('admin:admin_user_index'))


""" ----------------------------------------------------------------------
    View Team Admin
-----------------------------------------------------------------------"""


class AdminTeamIndex(ListView):
    model = Team
    template_name = 'team/admin/admin_team_index.html'
    paginate_by = 15
    context_object_name = 'list_team'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team Index'
        return super(AdminTeamIndex, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search is None:
            return Team.objects.all()
        else:
            return Team.objects.filter(Q(name__icontains=search) | Q(about_team__icontains=search))

    def get_context_data(self, **kwargs):
        ctx = super(AdminTeamIndex, self).get_context_data(**kwargs)
        for team in ctx['list_team']:
            # team.leader_user = return_user(team.leader)
            team.total_skill = return_total_skill_of_team(team)
        return ctx


AdminTeamIndexView = AdminTeamIndex.as_view()


class AdminTeamCreate(CreateView):
    model = Team
    template_name = 'team/admin/admin_team_create.html'
    form_class = TeamCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Create new team'
        return super(AdminTeamCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_team_index')

    def form_valid(self, form):
        team = form.save()
        team.leader = User.objects.get(id=1)
        team.save()
        # profile = Profile.objects.get(user=team.leader)
        # profile.team = team
        # profile.save()
        return super().form_valid(form)


AdminTeamCreateView = AdminTeamCreate.as_view()


class AdminTeamDetail(DetailView):
    model = Team
    template_name = 'team/admin/admin_team_detail.html'
    context_object_name = 'detail_team'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team Detail'
        return super(AdminTeamDetail, self).dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return self.object.ge

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['leader'] = User.objects.get(id=self.object.leader.id)
        ctx['total_skill'] = return_total_skill_of_team(self.object)
        ctx['total_member'] = return_total_user_of_team(self.object)
        ctx['total_project'] = return_total_project_of_team(self.object)
        ctx['list_member_of_team'] = return_list_member_of_team(self.object)
        ctx['list_skill_of_team'] = return_list_skill_of_team(self.object)
        ctx['list_project_of_team'] = return_list_project_of_team(self.object)
        return ctx


AdminTeamDetailView = AdminTeamDetail.as_view()


class AdminTeamEdit(UpdateView):
    model = Team
    template_name = 'team/admin/admin_team_edit.html'
    context_object_name = 'edit_team'
    form_class = TeamEditFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team Edit'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_leader_team'] = return_list_member_leader(self.object)
        return ctx

    def form_valid(self, form):
        team = form.save(commit=False)
        """Get user id new leader"""
        id_new_leader = self.request.POST.get('id_leader', '')
        """Return old leader of team"""
        leader_team = return_leader_of_team(self.object)
        try:
            if id_new_leader != leader_team.id:
                """Set new leader of team"""
                team.leader = User.objects.get(id=id_new_leader)

                """Get Profile old leader team"""
                profile_leader_team = Profile.objects.get(user=User.objects.get(id=leader_team.id))

                """Get Profile new leader team"""
                profile_id_new_leader = Profile.objects.get(user=User.objects.get(id=id_new_leader))

                """Set Position old leader team"""
                profile_leader_team.position = Position.objects.get(id=2)  # Developer

                """Set Position new leader team"""
                profile_id_new_leader.position = Position.objects.get(id=3)  # Leader

                """Set new team of user"""
                profile_id_new_leader.team = self.object

                profile_leader_team.save(())
                profile_id_new_leader.save(())
                team.save()
                form.save()
        except:
            pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:admin_team_detail', kwargs={'slug': self.object.slug})


AdminTeamEditView = AdminTeamEdit.as_view()


class AdminTeamEditSkill(DetailView):
    model = Team
    template_name = 'team/admin/admin_team_edit_skill.html'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team update skill'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AdminTeamEditSkill, self).get_context_data(**kwargs)
        ctx['list_skill_of_team'] = return_list_skill_of_team(self.object)
        ctx['list_skill_not_of_team'] = return_list_skill_not_of_team(self.object)
        return ctx


AdminTeamEditSkillView = AdminTeamEditSkill.as_view()


def add_skill_team(request):
    id_skill = request.POST.get('id_skill', None)
    id_team = request.POST.get('id_team', None)
    if id_team is not None:
        if id_skill is None:
            return HttpResponseRedirect(reverse('admin:admin_team_edit_skill', kwargs={'slug': Team.objects.get(id=id_team).slug}))
        else:
            skill = Skill.objects.get(id=id_skill)
            skill.team.add(Team.objects.get(id=id_team))
            skill.save()
            return HttpResponseRedirect(reverse('admin:admin_team_edit_skill', kwargs={'slug': Team.objects.get(id=id_team).slug}))
    else:
        return HttpResponseRedirect(reverse('admin:admin_team_index'))


def admin_team_delete(request):
    id_team = request.POST.get('id_team', None)
    if id_team is not None:
        """Return id team delete"""
        team = get_object_or_404(Team, pk=id_team)

        """Return team None ( Default )"""
        team_none = Team.objects.get(name='None')

        """Return team leader"""
        team_leader = return_leader_of_team(team)

        """Set team leader -> team_none"""
        team_leader.team = team_none
        team_leader.position = Position.objects.get(name='None')
        team_leader.save()
        """Return list member of team"""
        list_member = return_list_member_of_team(team)

        """Set list member -> team_none"""
        set_team_list_user(list_member, team_none)

        """Delete team"""
        team.delete()

        return HttpResponseRedirect(reverse('admin:admin_team_index'))
    else:
        return HttpResponseRedirect(reverse('admin:admin_team_index'))


""" ----------------------------------------------------------------------
    View Project Admin
-----------------------------------------------------------------------"""


class AdminProjectIndex(ListView):
    model = Project
    template_name = 'project/admin/admin_project_index.html'
    paginate_by = 15
    context_object_name = 'list_project'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Project Index'
        return super(AdminProjectIndex, self).dispatch(request, *args, **kwargs)


AdminProjectIndexView = AdminProjectIndex.as_view()


class AdminProjectCreate(CreateView):
    model = Project
    template_name = 'project/admin/admin_project_create.html'
    form_class = ProjectCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Create new project'
        return super(AdminProjectCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_project_index')


AdminProjectCreateView = AdminProjectCreate.as_view()


class AdminProjectDetail(DetailView):
    model = Project
    template_name = 'project/admin/admin_project_detail.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Project Detail'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if ctx['object'].status == 0:
            ctx['object'].status = 'Fail'
        elif ctx['object'].status == 1:
            ctx['object'].status = 'Success'
        elif ctx['object'].status == 2:
            ctx['object'].status = 'Progress'
        elif ctx['object'].status == 3:
            ctx['object'].status = 'Begin'
        ctx['object'].total_team = return_total_team_of_project(self.object)
        ctx['list_team_of_project'] = return_list_team_of_project(self.object)
        return ctx


AdminProjectDetailView = AdminProjectDetail.as_view()


class AdminProjectEdit(UpdateView):
    model = Project
    template_name = 'project/admin/admin_project_edit.html'
    form_class = ProjectCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Project Edit'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_leader_project'] = return_list_leader_of_project(self.object)
        return ctx

    def form_valid(self, form):
        pro = form.save(commit=False)
        id_leader = self.request.POST.get('id_leader', None)
        pro.leader = User.objects.get(id=id_leader)
        pro.save()
        form.save()
        return super().form_valid(form)


AdminProjectEditView = AdminProjectEdit.as_view()


class AdminProjectEditTeam(DetailView):
    model = Project
    template_name = 'project/admin/admin_project_edit_team.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Project Team'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_team_of_project'] = return_list_team_of_project(self.object)
        ctx['list_team_not_of_project'] = return_list_team_not_of_project(self.object)
        ctx['status'] = self.object.status
        return ctx


AdminProjectEditTeamView = AdminProjectEditTeam.as_view()


def add_team_project(request):
    id_project = request.POST.get('id_project', None)
    id_team = request.POST.get('id_team', None)
    if id_project is not None and id_team is not None:
        try:
            team = get_object_or_404(Team, id=id_team)
            project = get_object_or_404(Project, id=id_project)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('admin:admin_project_index'))
        team_project, create = TeamProject.objects.get_or_create(team=team, project=project)
        team_project.status = True
        team_project.save()
        return HttpResponseRedirect(reverse('admin:admin_project_edit_team', kwargs={'slug': Project.objects.get(id=id_project).slug}))
    else:
        return HttpResponseRedirect(reverse('admin:admin_project_index'))


def remover_team_project(request):
    id_project = request.POST.get('id_project', None)
    id_team = request.POST.get('id_team', None)
    if id_project is not None and id_team is not None:
        try:
            team = get_object_or_404(Team, id=id_team)
            project = get_object_or_404(Project, id=id_project)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('admin:admin_project_index'))
        team_project, create = TeamProject.objects.get_or_create(team=team, project=project)
        team_project.delete()
        return HttpResponseRedirect(reverse('admin:admin_project_edit_team', kwargs={'slug': Project.objects.get(id=id_project).slug}))
    else:
        return HttpResponseRedirect(reverse('admin:admin_project_index'))


def admin_project_delete(request):
    id_project = request.POST.get('id_project', None)
    if id_project is not None:
        project = get_object_or_404(Project, pk=id_project)
        project.delete()
        return HttpResponseRedirect(reverse('admin:admin_project_index'))
    else:
        return HttpResponseRedirect(reverse('admin:admin_project_index'))


""" ----------------------------------------------------------------------
    View Skill Admin
-----------------------------------------------------------------------"""


class AdminSkillIndex(ListView):
    model = Skill
    template_name = 'skill/admin/admin_skill_index.html'
    paginate_by = 15
    context_object_name = 'list_skill'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Skill Index'
        return super(AdminSkillIndex, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for i in ctx['list_skill']:
            i.count_team = count_team_of_skill(i)
            i.count_user = count_user_of_skill(i)
        return ctx


AdminSkillIndexView = AdminSkillIndex.as_view()


class AdminSkillCreate(CreateView):
    model = Skill
    template_name = 'skill/admin/admin_skill_create.html'
    form_class = SkillCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Create new skill'
        return super(AdminSkillCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_skill_index')


AdminSkillCreateView = AdminSkillCreate.as_view()


class AdminSkillDetail(DetailView):
    model = Skill
    template_name = 'skill/admin/admin_skill_detail.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Skill Detail'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list_user_of_skill'] = return_list_user_of_skill(self.object)
        ctx['list_team_of_skill'] = return_list_team_of_skill(self.object)

        return ctx


AdminSkillDetailView = AdminSkillDetail.as_view()


class AdminSkillEdit(UpdateView):
    model = Skill
    template_name = 'skill/admin/admin_skill_edit.html'
    form_class = SkillCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Skill Edit'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['list_leader_team'] = return_list_member_leader(self.object)
        return ctx

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:admin_skill_detail', kwargs={'slug': self.object.slug})


AdminSkillEditView = AdminSkillEdit.as_view()


@requirement_admin
def admin_skill_delete(request):
    id_skill = request.POST.get('id_skill', None)
    if id_skill is not None:
        request.session['title'] = 'Skill Edit'
        skill = get_object_or_404(Skill, pk=id_skill)
        skill.delete()
        return HttpResponseRedirect(reverse('admin:admin_skill_index'))
    else:
        return HttpResponseRedirect(reverse('admin:admin_skill_index'))


""" ----------------------------------------------------------------------
    View Position Admin
-----------------------------------------------------------------------"""


class AdminPositionIndex(ListView):
    model = Position
    template_name = 'position/admin/admin_position_index.html'
    paginate_by = 15
    context_object_name = 'list_position'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Position Index'
        return super(AdminPositionIndex, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


AdminPositionIndexView = AdminPositionIndex.as_view()


class AdminPositionCreate(CreateView):
    model = Position
    template_name = 'position/admin/admin_position_create.html'
    form_class = PositionCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Create new Position'
        return super(AdminPositionCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_position_index')


AdminPositionCreateView = AdminPositionCreate.as_view()


class AdminPositionDetail(DetailView):
    model = Position
    template_name = 'position/admin/admin_position_detail.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Position Detail'
        return super().dispatch(request, *args, **kwargs)


AdminPositionDetailView = AdminPositionDetail.as_view()


class AdminPositionEdit(UpdateView):
    model = Position
    template_name = 'position/admin/admin_position_edit.html'
    form_class = PositionCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Position Edit'
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_position_index')


AdminPositionEditView = AdminPositionEdit.as_view()


@requirement_admin
def admin_delete_position(request):
    id_position = request.POST.get('id_position', None)
    if id_position is not None:
        request.session['title'] = 'Position Edit'
        list_user = return_list_user_of_position(Position.objects.get(pk=id_position))
        set_position_list_user(list_user, 1)
        Position.objects.get(pk=id_position).delete()
        return HttpResponseRedirect(reverse('admin:admin_position_index'))
    else:
        return HttpResponseRedirect(reverse('admin:admin_position_index'))


"""--------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------"""


class ProfileExport(View):
    def get(self, *args, **kwargs):
        dataset = CountryResource().export()
        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=profile.csv'
        return response


class ProfileImport(View):
    model = Profile
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'admin/user/import.html'
    resource_class = None

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def get(self, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        # if self.request.POST and form.is_valid():
        #     input_format = import_formats[
        #         int(form.cleaned_data['input_format'])
        #     ]()
        #     import_file = form.cleaned_data['import_file']
        #     # first always write the uploaded file to disk as it may be a
        #     # memory file or else based on settings upload handlers
        #     with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
        #         for chunk in import_file.chunks():
        #             uploaded_file.write(chunk)
        #
        #     # then read the file, using the proper format-specific mode
        #     with open(uploaded_file.name,
        #               input_format.get_read_mode()) as uploaded_import_file:
        #         # warning, big files may exceed memory
        #         data = uploaded_import_file.read()
        #         if not input_format.is_binary() and self.from_encoding:
        #             data = force_text(data, self.from_encoding)
        #         dataset = input_format.create_dataset(data)
        #         result = resource.import_data(dataset, dry_run=True,
        #                                       raise_errors=False)
        #
        #     context['result'] = result
        #
        #     if not result.has_errors():
        #         context['confirm_form'] = ConfirmImportForm(initial={
        #             'import_file_name': os.path.basename(uploaded_file.name),
        #             'input_format': form.cleaned_data['input_format'],
        #         })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)

    def post(self, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                    'original_file_name': form.cleaned_data['import_file'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)


class ProfileProcessImport(View):
    model = Profile
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'admin/user/import.html'
    resource_class = None

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def post(self, *args, **kwargs):
        '''
        Perform the actual import action (after the user has confirmed he
    wishes to import)
        '''
        opts = self.model._meta
        resource = self.get_import_resource_class()()

        confirm_form = ConfirmImportForm(self.request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            import_file_name = os.path.join(
                tempfile.gettempdir(),
                confirm_form.cleaned_data['import_file_name']
            )
            import_file = open(import_file_name, input_format.get_read_mode())
            data = import_file.read()
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            result = resource.import_data(dataset, dry_run=False, raise_errors=True)

            # Add imported objects to LogEntry
            ADDITION = 1
            CHANGE = 2
            DELETION = 3
            logentry_map = {
                RowResult.IMPORT_TYPE_NEW: ADDITION,
                RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                RowResult.IMPORT_TYPE_DELETE: DELETION,
            }
            content_type_id = ContentType.objects.get_for_model(self.model).pk
            '''
            for row in result:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=content_type_id,
                    object_id=row.object_id,
                    object_repr=row.object_repr,
                    action_flag=logentry_map[row.import_type],
                    change_message="%s through import_export" % row.import_type,
                )
            '''
            success_message = 'Import finished'
            # messages.success(self.request, success_message)
            import_file.close()

            # url = reverse('%s_list' % (str(opts.app_label).lower()))
            url = reverse('admin:admin_user_index')
            return HttpResponseRedirect(url)
        else:
            print(confirm_form.clean_import_file_name())
            print(confirm_form)
            url = reverse('admin:admin_team_index')
            return HttpResponseRedirect(url)
