from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Show, NewsItem


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        results = NewsItem.objects.filter(
            published=True).order_by("-created")
        if results.count() > 0:
            context['latest_news'] = results[0]
        else:
            context['latest_news'] = None
        return context


class ShowDetails(DetailView):
    model = Show
