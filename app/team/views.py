# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from app.project.function import return_total_project_of_team, return_list_project_of_team

from app.skill.function import return_total_skill_of_team, return_list_skill_of_team
from app.team.function import return_total_user_of_team, return_list_member_of_team

from app.team.models import Team


class TeamIndex(ListView):
    model = Team
    paginate_by = 15
    template_name = 'team/user/index.html'
    context_object_name = 'list_team'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team Index'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search is None:
            return Team.objects.all()
        else:
            return Team.objects.filter(Q(name__icontains=search) | Q(about_team__icontains=search))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for team in ctx['list_team']:
            team.total_skill = return_total_skill_of_team(team)
        return ctx


TeamIndexView = TeamIndex.as_view()


class TeamDetail(DetailView):
    model = Team
    template_name = 'team/user/detail_team.html'
    context_object_name = 'detail_team'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Team Detail'
        return super().dispatch(request, *args, **kwargs)

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


TeamDetailView = TeamDetail.as_view()
