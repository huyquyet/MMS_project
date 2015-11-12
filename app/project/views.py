# Create your views here.
from django.views.generic import TemplateView


class ProjectIndex(TemplateView):
    template_name = 'project/user/index.html'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Project Index'
        return super().dispatch(request, *args, **kwargs)


ProjectIndexView = ProjectIndex.as_view()
