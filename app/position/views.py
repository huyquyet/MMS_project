# Create your views here.
from django.views.generic import TemplateView


class PositionIndex(TemplateView):
    template_name = 'position/user/index.html'

    def dispatch(self, request, *args, **kwargs):
        self.request.session['title'] = 'Position Index'
        return super().dispatch(request, *args, **kwargs)


PositionIndexView = PositionIndex.as_view()
