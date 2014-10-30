from django.views.generic.base import TemplateView
from django.views.generic import DetailView, View
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Show, NewsItem, ShowVideo, Picture


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


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


class EditView(LoggedInMixin, TemplateView):
    template_name = "edit/index.html"


class EditShowView(LoggedInMixin, View):
    template_name = "edit/show.html"

    def get(self, request, pk):
        return render(
            request, self.template_name,
            dict(show=get_object_or_404(Show, pk=pk))
        )

    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        show.title = request.POST.get('title', 'no title')
        show.year = request.POST.get('year', '')
        show.location = request.POST.get('location', '')
        show.description = request.POST.get('description', '')
        show.save()
        messages.success(request, "Show updated")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class AddVideoToShowView(LoggedInMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        ShowVideo.objects.create(
            show=show, youtube_id=request.POST.get('youtube_id', ''))
        messages.success(request, "video added to show")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class DeleteShowVideoView(LoggedInMixin, DeleteView):
    model = ShowVideo
    success_url = "/edit/"


class DeletePictureView(LoggedInMixin, DeleteView):
    model = Picture
    success_url = "/edit/"
