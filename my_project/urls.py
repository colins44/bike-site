"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from bike_aggregator.views import Index, SignUp, ContactView, SorryNoBikesAvalibleView, StoreSignUp

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^bikes-to-rent/', Index.as_view(), name='index'),
    url(r'^bicycles-to-rent/', Index.as_view(), name='index'),
    url(r'^contact/', ContactView.as_view(), name='contact'),
    url(r'^sign-up/', SignUp.as_view(), name='index'),
    url(r'^sorry-no-bikes-available/',
        SorryNoBikesAvalibleView.as_view(),
        name='sorry-no-bikes-available'),
    url(r'^thanks/',
        StoreSignUp.as_view(),
        name='thanks'),


]
