from django.conf.urls import patterns, url
import artsho.bidauth.views as views

urlpatterns = patterns(
    '',
    url(r'^login/$', views.LoginView.as_view(), name='bidauth_login'),
)
