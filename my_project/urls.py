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
    BikeShopContact, EnquiryEmailSent, map, Index, BikeSearchResults, BikeSearchResultsMapView, NewsLetterSignUp, \
    SearchPopularityChart, BikeShopGeoChart, SearchesOverTimeChart, StockListView, \
    StockDetailView, StockCreateView, StockDeleteView, StockUpdateView, ShopDetailView, ShopCreateView, ShopDeleteView, \
    ShopUpdateView, BikeShopView, BikeShopRedirectView
from bike_aggregator.sitemaps import StaticSiteMap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

sitemaps ={
    'mysitemap':StaticSiteMap
}

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bike-shop-search-results/(?P<latitude>[-\S]+)/(?P<longitude>[-\S]+)/$',
        BikeSearchResults.as_view(), name='bike-shop-search-results'),
    url(r'^bike-shop-search-results-map-view/(?P<latitude>[-\S]+)/(?P<longitude>[-\S]+)/$',
        BikeSearchResultsMapView.as_view(), name='bike-shop-search-results-map-view'),
    url(r'^contact/', ContactView.as_view(), name='contact'),
    url(r'^contact-bikeshop/(?P<pk>[0-9]+)/', BikeShopContact.as_view(), name='bikeshop-contact'),
    url(r'^redirect-to-bikeshop/(?P<pk>[0-9]+)/', BikeShopRedirectView.as_view(), name='bikeshop-redirect'),
    url(r'^thanks/', StoreSignUp.as_view(), name='thanks'),
    url(r'^enquiry-email-sent/', EnquiryEmailSent.as_view(), name='enquiry-email-sent'),
    url(r'^find-out-more/', NewsLetterSignUp.as_view(), name='find-out-more'),
    url(r'^geo-shop-chart/', BikeShopGeoChart.as_view(), name='geo-shop-chart'),
    url(r'^geo-search-chart/', SearchPopularityChart.as_view(), name='geo-search-chart'),
    url(r'^geo-shop-chart/', BikeShopGeoChart.as_view(), name='geo-shop-chart'),
    url(r'^map/', TemplateView.as_view(template_name="bike-shop-list-map-view.html")),
    url(r'^map-points.json', map, name='map'),
    url(r'^robots\.txt', include('robots.urls'), name='robots'),
    url(r'^route-plot/', TemplateView.as_view(template_name="route-plot.html")),
    url(r'^search-over-time-chart/', SearchesOverTimeChart.as_view(), name='geo-shop-chart'),
    url(r'^sign-up/', SignUp.as_view(), name='sign-up'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(regex='^stock/list/$', view=login_required(StockListView.as_view()), name='stock-list'),
    url(regex='^stock/detail/(?P<pk>[0-9]+)/$', view=login_required(StockDetailView.as_view()), name='stock-detail'),
    url(regex='^stock/create/$', view=login_required(StockCreateView.as_view()), name='stock-create'),
    url(regex='^stock/delete/(?P<pk>[0-9]+)/$', view=login_required(StockDeleteView.as_view()), name='stock-delete'),
    url(regex='^stock/update/(?P<pk>[0-9]+)/$', view=login_required(StockUpdateView.as_view()), name='stock-update'),

    url(regex='^shop-profile/(?P<pk>[0-9]+)/$', view=BikeShopView.as_view(), name='shop-profile'),

    url(regex='^profile/$', view=login_required(ShopDetailView.as_view()), name='shop-detail'),
    url(regex='^profile/create/$', view=login_required(ShopCreateView.as_view()), name='shop-create'),
    url(regex='^profile/delete/(?P<pk>[0-9]+)/$', view=login_required(ShopDeleteView.as_view()), name='shop-delete'),
    url(regex='^profile/update/(?P<pk>[0-9]+)/$', view=login_required(ShopUpdateView.as_view()), name='shop-update'),

]
