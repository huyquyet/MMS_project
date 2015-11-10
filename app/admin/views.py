from django.contrib import auth
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView, UpdateView
from app.admin.forms import TeamCreateFormView, ProjectCreateFormView, SkillCreateFormView, PositionCreateFormView, UserCreateFormView, UserUpdateFormView
from app.position.models import Position
from app.project.function import return_total_project_of_team, return_list_project_of_team
from app.project.models import Project
from app.skill.function import return_total_skill_of_team, count_user_of_skill, count_team_of_skill, count_skill_of_user, return_list_skill_of_user, return_list_skill_not_of_user, return_list_skill_of_team
from app.skill.models import Skill, UserSkill
from app.team.function import return_total_user_of_team, return_list_member_of_team
from app.team.models import Team
from app.user.function import return_team_of_user, return_position_of_user
from app.user.models import Profile

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


    # def dispatch(self, request, *args, **kwargs):
    #     self.request.session['title'] = 'Admin index'
    #     super().dispatch(request, *args, **kwargs)

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
        user = form.save(commit=True)
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
