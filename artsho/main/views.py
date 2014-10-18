from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Show

class IndexView(TemplateView):
    template_name = "main/index.html"


class ShowDetails(DetailView):
    model = Show
