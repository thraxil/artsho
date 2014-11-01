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

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['drafts'] = NewsItem.objects.filter(
            published=False).count()
        context['published'] = NewsItem.objects.filter(
            published=True).count()
        return context


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
        show.update_video_order()
        ShowVideo.objects.create(
            show=show, youtube_id=request.POST.get('youtube_id', ''))
        messages.success(request, "video added to show")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class AddPictureView(LoggedInMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        show.update_picture_order()
        p = Picture.objects.create(show=show)
        p.save_image(request.FILES['image'])
        messages.success(request, "picture added to show")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class DeleteShowVideoView(LoggedInMixin, DeleteView):
    model = ShowVideo
    success_url = "/edit/"

    def get_success_url(self):
        return reverse('edit_show', args=[self.object.show.id])


class DeletePictureView(LoggedInMixin, DeleteView):
    model = Picture
    success_url = "/edit/"

    def get_success_url(self):
        return reverse('edit_show', args=[self.object.show.id])


class AddNewsView(LoggedInMixin, View):
    template_name = "edit/add_news.html"

    def get(self, request):
        return render(
            request, self.template_name,
            dict())

    def post(self, request):
        ni = NewsItem.objects.create(
            title=request.POST.get('title', 'title is required'),
            topcontent=request.POST.get('topcontent', ''),
            content=request.POST.get('content', ''),
            published=False,
        )
        messages.success(request, "news item added")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class NewsDraftsView(LoggedInMixin, TemplateView):
    template_name = "edit/news_drafts.html"

    def get_context_data(self, **kwargs):
        context = super(NewsDraftsView, self).get_context_data(**kwargs)
        results = NewsItem.objects.filter(
            published=False).order_by("-created")
        context['drafts'] = results
        return context


class NewsArchiveView(LoggedInMixin, TemplateView):
    template_name = "edit/news_archive.html"

    def get_context_data(self, **kwargs):
        context = super(NewsArchiveView, self).get_context_data(**kwargs)
        results = NewsItem.objects.filter(
            published=True).order_by("-created")
        context['items'] = results
        return context


class EditNewsItemView(LoggedInMixin, View):
    template_name = "edit/news_item.html"

    def get(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        return render(
            request, self.template_name,
            dict(item=ni)
        )

    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        ni.title = request.POST.get('title', 'title is required')
        ni.content = request.POST.get('content', '')
        ni.topcontent = request.POST.get('topcontent', '')
        ni.save()
        messages.success(request, "news item edited")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class PublishNewsItemView(LoggedInMixin, View):
    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        ni.published = True
        ni.save()
        messages.success(request, "news item published")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class RevertNewsItemView(LoggedInMixin, View):
    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        ni.published = False
        ni.save()
        messages.success(request, "news item reverted to draft")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class DeleteNewsItemView(LoggedInMixin, DeleteView):
    model = NewsItem
    success_url = "/edit/"
