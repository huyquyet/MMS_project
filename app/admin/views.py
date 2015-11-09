from django.contrib import auth
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView
from app.admin.forms import TeamCreateFormView, ProjectCreateFormView, SkillCreateFormView
from app.project.models import Project
from app.skill.function import return_total_skill_of_team, count_user_of_skill, count_team_of_skill
from app.skill.models import Skill
from app.team.models import Team

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
