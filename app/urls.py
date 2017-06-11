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
from app.views import Dashboard, Home, FinancierUpdateAccount, OurProducts, PVT, \
SolarComponent, SolarGeyser, Register, UserRoleView


#from registration.backends.default.views import RegistrationView

#from app.views import Registration


urlpatterns = [
    url(r'^\Z', Home.as_view(), name='home'),
    #url(r'^\Z', Dashboard.as_view(), name='dashboard'),
    url(r'^app/$', Dashboard.as_view(), name='dashboard'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^financier/$', FinancierUpdateAccount.as_view(), name='financier'),
    url(r'^user_roles/$', UserRoleView.as_view(), name='user_roles'),
    url(r'^home/products/', OurProducts.as_view(), name='our_products'),
    url(r'^home/products/pvt/', PVT.as_view(), name='pvt'),
    url(r'^home/products/geyser/', SolarGeyser.as_view(), name='geyser'),
    url(r'^home/products/component/', SolarComponent.as_view(), name='component'),
    url(r'^home/register/', Register.as_view(), name='register'),

    #url(r'^register/$', Registration.as_view()),

    #url(r'^accounts/', include('registration.backends.default.urls')),

]
