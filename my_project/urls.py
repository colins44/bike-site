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
from django.contrib.auth.decorators import login_required

from bike_aggregator.views import SignUp, ContactView, StoreSignUp, \
    BikeShopContact,  Index, BikeSearchResults, StockListView, \
    StockDetailView, StockCreateView, StockDeleteView, StockUpdateView, ShopDetailView, ShopCreateView, ShopDeleteView, \
    ShopUpdateView, BikeShopView, BookingDetailView, BookingListView, bikeshopdetail
from bike_aggregator.sitemaps import StaticSiteMap
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views

import brillixy.site
brillixy.site.setup(admin.site)

sitemaps ={
    'mysitemap':StaticSiteMap
}

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bike-shop-search-results/(?P<latitude>[-\S]+)/(?P<longitude>[-\S]+)/$',
        BikeSearchResults.as_view(), name='bike-shop-search-results'),
    url(r'^bike-shop-search-results/(?P<city>[-\w]+)/$',
        BikeSearchResults.as_view(), name='bike-shop-search-results'),
    url(r'^contact/', ContactView.as_view(), name='contact'),
    url(r'^contact-bikeshop/(?P<pk>[0-9]+)/', BikeShopContact.as_view(), name='bikeshop-contact'),
    url(r'^bikeshop-details/(?P<pk>[0-9]+)/', bikeshopdetail, name='bikeshop-contact'),
    url(r'^thanks/', StoreSignUp.as_view(), name='thanks'),
    url(r'^robots\.txt', include('robots.urls'), name='robots'),
    url(r'^sign-up/', SignUp.as_view(), name='sign-up'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(regex='^stock/list/$', view=login_required(StockListView.as_view()), name='stock-list'),
    url(regex='^stock/detail/(?P<pk>[0-9]+)/$', view=login_required(StockDetailView.as_view()), name='stock-detail'),
    url(regex='^stock/create/$', view=login_required(StockCreateView.as_view()), name='stock-create'),
    url(regex='^stock/delete/(?P<pk>[0-9]+)/$', view=login_required(StockDeleteView.as_view()), name='stock-delete'),
    url(regex='^stock/update/(?P<pk>[0-9]+)/$', view=login_required(StockUpdateView.as_view()), name='stock-update'),

    url(regex='^booking/list/$', view=login_required(BookingListView.as_view()), name='booking-list'),
    url(regex='^booking/detail/(?P<pk>[0-9]+)/$', view=login_required(BookingDetailView.as_view()), name='booking-detail'),

    url(regex='^shop-profile/(?P<pk>[0-9]+)/$', view=BikeShopView.as_view(), name='shop-profile'),

    url(regex='^profile/$', view=login_required(ShopDetailView.as_view()), name='shop-detail'),
    url(regex='^profile/create/$', view=login_required(ShopCreateView.as_view()), name='shop-create'),
    url(regex='^profile/delete/(?P<pk>[0-9]+)/$', view=login_required(ShopDeleteView.as_view()), name='shop-delete'),
    url(regex='^profile/update/(?P<pk>[0-9]+)/$', view=login_required(ShopUpdateView.as_view()), name='shop-update'),

]
