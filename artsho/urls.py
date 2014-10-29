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

    url(r'^edit/$', views.EditView.as_view(), name='edit_index'),
    url(r'^edit/show/(?P<pk>\d+)/$',
        views.EditShowView.as_view(), name='edit_show'),
    url(r'^edit/show/(?P<pk>\d+)/add_video/$',
        views.AddVideoToShowView.as_view(), name='edit_show_add_video'),
    url(r'^edit/showvideo/(?P<pk>\d+)/delete/$',
        views.DeleteShowVideoView.as_view(), name='delete_show_video'),

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
