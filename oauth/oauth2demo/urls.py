from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.auth),
    url(r'^sequencing/authorize', views.auth_callback),
    url(r'^sequencing/authorization-approved', views.api, name="api"),
]
