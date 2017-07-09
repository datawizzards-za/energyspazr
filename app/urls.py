"""energyspazr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from app import views, api_views


urlpatterns = [
    url(r'^\Z', views.Home.as_view(), name='home'),
    url(r'^app/$', views.Home.as_view(), name='dashboard'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^user_account_update/$', views.UserAccountUpdate.as_view(),
        name='user_account_update'),
    url(r'^our-products/$', views.OurProducts.as_view(), name='our-products'),
    url(r'^my-products/$', views.MyProducts.as_view(), name='my-products'),
    url(r'^my-quotes/$', views.MyQuotes.as_view(), name='my-quotes'),
    url(r'^pvt-order/$', views.OrderPVTSystem.as_view(), name='pvt-order'),
    url(r'^geyser-order/$', views.OrderGeyser.as_view(), name='geyser-order'),
    url(r'^order-quotes/(?P<user_id>[0-9A-Fa-f-]+)/$', views.OrderQuotes.as_view(),
        name='order-quotes'),
    url(r'^component-order/$', views.SolarComponent.as_view(),
        name='component-order'),
    url(r'^add-component/$', views.AddComponent.as_view(),
        name='add-component'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^order/$', views.ClientOrder.as_view(), name='order'),
    url(r'^client-info/$', views.ClientOrder.as_view(), name='client-info'),
    url(r'^products/$', views.OurProducts.as_view(), name='our_products'),
    url(r'^products/component/$', views.SolarComponent.as_view(),
        name='component'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^view-slip/(?P<generate>[0-9A-Fa-f-]+)/$', views.DisplayPDF.as_view(),
        name='slips'),
    url(r'^api/list_solar_panels/$', api_views.ListSolarPanels.as_view(), 
        name='list_solar_panels'),
    url(r'api/get_brand/(?P<brand_id>\d+)/$', 
        api_views.GetProductBrand.as_view(), name='get_brand'),
]
