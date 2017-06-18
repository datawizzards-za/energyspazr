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
from app import views


urlpatterns = [
    url(r'^\Z', views.Home.as_view(), name='home'),
    url(r'^app/$', views.Home.as_view(), name='dashboard'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^user_account_update/$', views.UserAccountUpdate.as_view(),
        name='user_account_update'),
    url(r'^our-products/$', views.OurProducts.as_view(), name='our-products'),
    url(r'^my-products/$', views.MyProducts.as_view(), name='my-products'),
    url(r'^pvt-order/$', views.OrderPVTSystem.as_view(), name='pvt-order'),
    url(r'^geyser-order/$', views.OrderGeyser.as_view(), name='geyser-order'),
    url(r'^component-order/$', views.SolarComponent.as_view(),
        name='component-order'),
    url(r'^add-component/$', views.AddComponent.as_view(),
        name='add-component'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^order/$', views.ClientOrder.as_view(), name='order'),
    url(r'^client-info/$', views.ClientOrder.as_view(), name='client-info'),
    url(r'^products/$', views.OurProducts.as_view(), name='our_products'),
    url(r'^products/pvt/$', views.PVT.as_view(), name='pvt'),
    url(r'^products/geyser/$', views.SolarGeyser.as_view(), name='geyser'),
    url(r'^products/component/$', views.SolarComponent.as_view(),
        name='component'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^view-slip/$', views.DisplayPDF.as_view(), name='slips'),
]
