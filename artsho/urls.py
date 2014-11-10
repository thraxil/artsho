from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from artsho.main import views
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^$', views.IndexView.as_view()),

    (r'^about/$', TemplateView.as_view(template_name="main/about.html")),
    (r'^map/$', TemplateView.as_view(template_name="main/map.html")),
    (r'^contact/$', TemplateView.as_view(template_name="main/contact.html")),

    (r'^artsho/(?P<pk>\d+)/$', views.ShowDetails.as_view()),

    url(r'^auction/(?P<pk>\d+)/$', views.AuctionDetailsView.as_view(),
        name='auction_details'),

    url(r'^edit/$', views.EditView.as_view(), name='edit_index'),

    url(r'^edit/add_news/$', views.AddNewsView.as_view(), name='add_news'),
    url(r'^edit/news/drafts/$', views.NewsDraftsView.as_view(),
        name='news_drafts'),
    url(r'^edit/news/$', views.NewsArchiveView.as_view(),
        name='news_archive'),
    url(r'^edit/news/(?P<pk>\d+)/$', views.EditNewsItemView.as_view(),
        name='edit_news_item'),
    url(r'^edit/news/(?P<pk>\d+)/add_picture/$',
        views.AddNewsPicture.as_view(),
        name='add_news_picture'),

    url(r'^edit/news/(?P<pk>\d+)/preview/$',
        views.PreviewNewsItemView.as_view(),
        name='preview_news_item'),

    url(r'^edit/news/(?P<pk>\d+)/publish/$',
        views.PublishNewsItemView.as_view(),
        name='publish_news_item'),
    url(r'^edit/news/(?P<pk>\d+)/revert/$', views.RevertNewsItemView.as_view(),
        name='revert_news_item'),
    url(r'^edit/news/(?P<pk>\d+)/delete/$', views.DeleteNewsItemView.as_view(),
        name='delete_news_item'),

    url(r'^edit/show/(?P<pk>\d+)/$',
        views.EditShowView.as_view(), name='edit_show'),
    url(r'^edit/show/(?P<pk>\d+)/add_video/$',
        views.AddVideoToShowView.as_view(), name='edit_show_add_video'),
    url(r'^edit/show/(?P<pk>\d+)/reorder_pictures/$',
        views.ReorderShowPicturesView.as_view(), name='reorder_show_pictures'),
    url(r'^edit/show/(?P<pk>\d+)/reorder_videos/$',
        views.ReorderShowVideosView.as_view(), name='reorder_show_videos'),

    url(r'^edit/show/(?P<pk>\d+)/add_picture/$',
        views.AddPictureView.as_view(), name='edit_show_add_picture'),

    url(r'^edit/show/(?P<pk>\d+)/add_auction/$',
        views.AddAuctionView.as_view(), name='add_auction'),

    url(r'^edit/showvideo/(?P<pk>\d+)/delete/$',
        views.DeleteShowVideoView.as_view(), name='delete_show_video'),
    url(r'^edit/picture/(?P<pk>\d+)/delete/$',
        views.DeletePictureView.as_view(), name='delete_picture'),
    url(r'^edit/newspicture/(?P<pk>\d+)/delete/$',
        views.DeleteNewsPictureView.as_view(), name='delete_newspicture'),

    url(r'^edit/auction/(?P<pk>\d+)/$',
        views.EditAuctionView.as_view(), name='edit_auction'),
    url(r'^edit/auction/(?P<pk>\d+)/end/$',
        views.EndAuctionView.as_view(), name='end_auction'),
    url(r'^edit/auction/(?P<pk>\d+)/start/$',
        views.StartAuctionView.as_view(), name='start_auction'),
    url(r'^edit/auction/(?P<pk>\d+)/add_item/$',
        views.AddItemToAuctionView.as_view(),
        name='add_item_to_auction'),

    url(r'^edit/item/(?P<pk>\d+)/$',
        views.EditAuctionItemView.as_view(),
        name='edit_auction_item'),
    url(r'^edit/item/(?P<pk>\d+)/delete/$',
        views.DeleteItemView.as_view(),
        name='delete_item'),
    url(r'^edit/itemartist/(?P<pk>\d+)/delete/$',
        views.DeleteItemArtistView.as_view(),
        name='remove_artist_from_item'),

    (r'^bidauth/', include('artsho.bidauth.urls')),

    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'infranil/', include('infranil.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
