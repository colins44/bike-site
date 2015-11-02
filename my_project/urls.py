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
from bike_aggregator.views import Control, SignUp, ContactView, SorryNoBikesAvalibleView, StoreSignUp, Test, index, \
    BikeShopsView, BikeShopContact, EnquiryEmailSent
from bike_aggregator.sitemaps import StaticSiteMap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

sitemaps ={
    'mysitemap':StaticSiteMap
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', BikeShopsView.as_view(), name='index'),
    url(r'^bikes-to-rent/', Control.as_view(), name='control'),
    url(r'^bicycles-to-rent/', Test.as_view(), name='test'),
    url(r'^contact/', ContactView.as_view(), name='contact'),
    url(r'^sign-up/', SignUp.as_view(), name='sign-up'),
    url(r'^bike-shops/', BikeShopsView.as_view(), name='bike-shops'),
    url(r'^contact-bikeshop/(?P<pk>[0-9]+)/', BikeShopContact.as_view(), name='bikeshop-contact'),
    url(r'^sorry-no-bikes-available/', SorryNoBikesAvalibleView.as_view(), name='sorry-no-bikes-available'),
    url(r'^thanks/', StoreSignUp.as_view(), name='thanks'),
    url(r'^enquiry-email-sent/', EnquiryEmailSent.as_view(), name='enquiry-email-sent'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt', include('robots.urls'), name='robots'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
]
