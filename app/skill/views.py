# Create your views here.
from django.views.generic import TemplateView


class SkillIndex(TemplateView):
    template_name = 'skill/user/index.html'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Skill Index'
        return super().dispatch(request, *args, **kwargs)


SkillIndexView = SkillIndex.as_view()
