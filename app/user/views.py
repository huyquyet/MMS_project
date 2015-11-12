# Create your views here.
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView, UpdateView

from app.admin.forms import UserUpdateForm
from app.skill.function import return_list_skill_of_user
from app.skill.function import count_skill_of_user
from app.user.function import return_team_of_user, return_current_project_of_user
from app.user.function import return_position_of_user
from app.user.models import Profile


def userindex(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('team:team_index'))
    else:
        return HttpResponseRedirect(reverse('user:user_login'))


class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = 'user/user_login.html'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Login page'
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('team:team_index'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_form = form.get_user()
        login(self.request, user_form)
        return super(UserLogin, self).form_valid(form)

    def get_success_url(self):
        link = self.request.POST.get('next', '')
        if link:
            return link
        else:
            return reverse('user:user_index')


UserLoginView = UserLogin.as_view()


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:user_index'))


class UserEditProfile(UpdateView):
    model = Profile
    template_name = 'user/user_edit_profile.html'
    form_class = UserUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Profile Update'
        self.object = self.get_object()
        if self.object.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UserEditProfile, self).get_initial()
        initial['email'] = self.object.user.email
        initial['first_name'] = self.object.user.first_name
        initial['last_name'] = self.object.user.last_name
        initial['email_confirm'] = self.object.user.email
        return initial

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        profile = form.save()
        user = self.request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user:user_index')


UserEditProfileView = UserEditProfile.as_view()


class UserChangePass(UpdateView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/user_change_pass.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(UserChangePass, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object
        del kwargs['instance']
        return kwargs

    def get_success_url(self):
        # return reverse('user:user_edit_profile', kwargs={'pk': self.object.pk})
        return reverse('user:user_login')


UserChangePassView = UserChangePass.as_view()


class UserMemberIndex(ListView):
    model = User
    template_name = 'user/user/index.html'
    paginate_by = 12

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Member Index'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search is None:
            return User.objects.all()
        else:
            return User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(profile__team__name__icontains=search))


UserMemberIndexView = UserMemberIndex.as_view()


class UserMemberDetail(DetailView):
    model = User
    template_name = 'user/user/member_detail.html'
    context_object_name = 'detail_user'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Member detail'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['detail_user'].team = return_team_of_user(ctx['detail_user'])
        ctx['detail_user'].position = return_position_of_user(ctx['detail_user'])
        ctx['detail_user'].skill = count_skill_of_user(ctx['detail_user'])
        ctx['list_skill_user'] = return_list_skill_of_user(ctx['detail_user'])
        ctx['current_project'] = return_current_project_of_user(ctx['detail_user'])
        return ctx


UserMemberDetailView = UserMemberDetail.as_view()
