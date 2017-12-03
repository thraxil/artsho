# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, View
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import (
    HttpResponseRedirect, HttpResponse, HttpResponseForbidden)
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse


from .models import (
    Show, NewsItem, ShowVideo, Picture, NewsPicture,
    save_image, Auction, Item, ItemPicture,
    ItemArtist, Artist, Bid
)


class StaffMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user or request.user.is_anonymous:
            return redirect_to_login(request.get_full_path(),
                                     settings.LOGIN_URL,
                                     REDIRECT_FIELD_NAME)
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(StaffMixin, self).dispatch(request, *args, **kwargs)


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


class EditView(StaffMixin, TemplateView):
    template_name = "edit/index.html"

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['drafts'] = NewsItem.objects.filter(
            published=False).count()
        context['published'] = NewsItem.objects.filter(
            published=True).count()
        return context


class EditShowView(StaffMixin, View):
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


class ReorderShowPicturesView(StaffMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        keys = [int(k[len('pic_'):]) for k in request.POST.keys()]
        keys.sort()
        sis = [int(request.POST["pic_%d" % k]) for k in keys]
        show.set_picture_order(sis)
        return HttpResponse("ok")


class ReorderAuctionItemsView(StaffMixin, View):
    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        keys = [int(k[len('item_'):]) for k in request.POST.keys()]
        keys.sort()
        sis = [int(request.POST["item_%d" % k]) for k in keys]
        auction.set_item_order(sis)
        return HttpResponse("ok")


class ReorderShowVideosView(StaffMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        keys = [int(k[len('video_'):]) for k in request.POST.keys()]
        keys.sort()
        sis = [int(request.POST["video_%d" % k]) for k in keys]
        show.set_showvideo_order(sis)
        return HttpResponse("ok")


class AddVideoToShowView(StaffMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        show.update_video_order()
        ShowVideo.objects.create(
            show=show, youtube_id=request.POST.get('youtube_id', ''))
        messages.success(request, "video added to show")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class AddPictureView(StaffMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        show.update_picture_order()
        p = Picture.objects.create(show=show,
                                   caption=request.POST.get('caption', ''))
        save_image(p, request.FILES['image'])
        messages.success(request, "picture added to show")
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class AddAuctionView(StaffMixin, View):
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        Auction.objects.create(
            show=show,
            start=request.POST['start'],
            end=request.POST['end'],
        )
        return HttpResponseRedirect(reverse('edit_show', args=[show.id]))


class DeleteShowVideoView(StaffMixin, DeleteView):
    model = ShowVideo
    success_url = "/edit/"

    def get_success_url(self):
        return reverse('edit_show', args=[self.object.show.id])


class DeleteItemPictureView(StaffMixin, DeleteView):
    model = ItemPicture

    def get_success_url(self):
        return reverse('edit_auction_item', args=[self.object.item.id])


class DeletePictureView(StaffMixin, DeleteView):
    model = Picture

    def get_success_url(self):
        return reverse('edit_show', args=[self.object.show.id])


class DeleteNewsPictureView(StaffMixin, DeleteView):
    model = NewsPicture

    def get_success_url(self):
        return reverse('edit_news_item', args=[self.object.newsitem.id])


class DeleteArtistView(StaffMixin, DeleteView):
    model = Artist
    success_url = "/edit/"


class AddNewsView(StaffMixin, View):
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


class NewsDraftsView(StaffMixin, TemplateView):
    template_name = "edit/news_drafts.html"

    def get_context_data(self, **kwargs):
        context = super(NewsDraftsView, self).get_context_data(**kwargs)
        results = NewsItem.objects.filter(
            published=False).order_by("-created")
        context['drafts'] = results
        return context


class NewsArchiveView(StaffMixin, TemplateView):
    template_name = "edit/news_archive.html"

    def get_context_data(self, **kwargs):
        context = super(NewsArchiveView, self).get_context_data(**kwargs)
        results = NewsItem.objects.filter(
            published=True).order_by("-created")
        context['items'] = results
        return context


class PreviewNewsItemView(StaffMixin, DetailView):
    model = NewsItem
    template_name = "edit/preview_news_item.html"


class AddNewsPicture(StaffMixin, View):
    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        p = NewsPicture.objects.create(newsitem=ni)
        save_image(p, request.FILES['image'])
        messages.success(request, "picture added to news item")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class EditNewsItemView(StaffMixin, View):
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


class PublishNewsItemView(StaffMixin, View):
    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        ni.published = True
        ni.save()
        messages.success(request, "news item published")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class RevertNewsItemView(StaffMixin, View):
    def post(self, request, pk):
        ni = get_object_or_404(NewsItem, pk=pk)
        ni.published = False
        ni.save()
        messages.success(request, "news item reverted to draft")
        return HttpResponseRedirect(reverse('edit_news_item', args=[ni.id]))


class DeleteNewsItemView(StaffMixin, DeleteView):
    model = NewsItem
    success_url = "/edit/"


class AuctionDetailsView(DetailView):
    model = Auction


class AuctionDashboardView(StaffMixin, DetailView):
    model = Auction
    template_name = "main/auction_dashboard.html"


class AuctionBroadcastView(StaffMixin, View):
    def post(self, request, pk):
        a = get_object_or_404(Auction, pk=pk)
        a.send_broadcast_message(
            request.POST.get('subject', 'artsho message'),
            request.POST.get('body', ''))
        return HttpResponseRedirect(
            reverse('auction_dashboard', args=[a.id]))


class ItemDetailsView(DetailView):
    model = Item


class BidOnItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if request.user.is_anonymous:
            return HttpResponse("you must login before you can bid")
        try:
            bid = request.POST.get('bid', '0')
            bid = int(float(bid))
        except ValueError:
            messages.warning(
                request,
                "oops! we couldn't parse that bid as a number.")
            return HttpResponseRedirect(
                reverse('item_details', args=[item.id]))
        if bid > item.high_bid():
            b = Bid.objects.create(
                item=item,
                user=request.user,
                amount=bid
            )
            messages.success(request, u"you bid €%d on this item" % bid)
            b.send_confirmation_email()
            b.email_previous_bidders()
        else:
            messages.warning(
                request, (
                    "the bid you entered was lower than the current"
                    " high bid, so it was ignored. Please try again.")
                )
        return HttpResponseRedirect(
            reverse('item_details', args=[item.id]))


class EditAuctionView(StaffMixin, View):
    template_name = "edit/auction.html"

    def get(self, request, pk):
        return render(
            request, self.template_name,
            dict(auction=get_object_or_404(Auction, pk=pk))
        )

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        auction.start = request.POST.get('start', '')
        auction.end = request.POST.get('end', '')
        auction.description = request.POST.get('description', '')
        auction.save()
        messages.success(request, "Auction updated")
        return HttpResponseRedirect(
            reverse('edit_auction', args=[auction.id]))


class EditArtistView(StaffMixin, View):
    template_name = "edit/artist.html"

    def get(self, request, pk):
        return render(
            request, self.template_name,
            dict(artist=get_object_or_404(Artist, pk=pk))
        )

    def post(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        artist.name = request.POST.get('name', '')
        artist.bio = request.POST.get('bio', '')
        artist.save()
        messages.success(request, "Artist updated")
        return HttpResponseRedirect(
            reverse('edit_artist', args=[artist.id]))


class EndAuctionView(StaffMixin, View):
    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        auction.status = 'completed'
        auction.save()
        auction.send_end_of_auction_emails()
        messages.success(request, "Auction closed")
        return HttpResponseRedirect(
            reverse('edit_auction', args=[auction.id]))


class StartAuctionView(StaffMixin, View):
    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        auction.status = 'ongoing'
        auction.save()
        messages.success(request, "Auction opened")
        return HttpResponseRedirect(
            reverse('edit_auction', args=[auction.id]))


class AddItemToAuctionView(StaffMixin, View):
    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        i = Item.objects.create(
            auction=auction,
            title=request.POST.get('title', 'untitled'),
            description=request.POST.get('description', ''),
            medium=request.POST.get('medium', ''),
            starting_bid=request.POST.get('starting_bid', 0),
        )
        i.add_artist_by_name(request.POST.get('artist', ""))
        i.add_artist_by_name(request.POST.get('artist2', ""))
        messages.success(request, 'added auction item')
        return HttpResponseRedirect(reverse('edit_auction', args=[auction.id]))


class EditItemView(StaffMixin, View):
    template_name = "edit/item.html"

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(request, self.template_name,
                      dict(ai=item, all_artists=Artist.objects.all()))

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.title = request.POST.get('title', 'untitled')
        item.description = request.POST.get('description', '')
        item.medium = request.POST.get('medium', '')
        item.starting_bid = request.POST.get('starting_bid', 0)
        item.save()
        messages.success(request, "updated auction item")
        return HttpResponseRedirect(
            reverse('edit_auction_item', args=[item.id]))


class DeleteItemView(StaffMixin, DeleteView):
    model = Item

    def get_success_url(self):
        return reverse('edit_auction', args=[self.object.auction.id])


class AddArtistToItemView(StaffMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        artist_id = request.POST.get('artist_id', '')
        if artist_id == "":
            item.add_artist_by_name(name=request.POST.get('name', ''))
        else:
            a = get_object_or_404(Artist, pk=artist_id)
            item.add_artist_by_name(a.name)
        messages.success(request, "added artist")
        return HttpResponseRedirect(
            reverse('edit_auction_item', args=[item.id]))


class DeleteItemArtistView(StaffMixin, DeleteView):
    model = ItemArtist

    def get_success_url(self):
        return reverse('edit_auction_item', args=[self.object.item.id])


class DeleteAuctionItemView(StaffMixin, DeleteView):
    model = Item

    def get_success_url(self):
        return reverse('edit_auction', args=[self.object.auction.id])


class AddItemPictureView(StaffMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.update_picture_order()
        p = ItemPicture.objects.create(item=item)
        save_image(p, request.FILES['image'])
        messages.success(request, "picture added to item")
        return HttpResponseRedirect(
            reverse('edit_auction_item', args=[item.id]))
