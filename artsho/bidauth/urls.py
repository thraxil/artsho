from django.conf.urls import url
import artsho.bidauth.views as views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='bidauth_login'),
]
