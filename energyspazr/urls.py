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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.forms import SigninForm, SignupForm, PVTOrderForm
from registration.backends.hmac.views import RegistrationView
from app.views import FinancierUpdateAccount, OrderPVTSystem

urlpatterns = [
    url(r'^\Z', include('app.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^app/financier/', FinancierUpdateAccount.as_view(),
        name='financier'),
    url(r'^app/pvt_order/', OrderPVTSystem.as_view(),
        name='pvt_order'),
    url(r'^accounts/signin/$', auth_views.login,
        {'template_name': 'registration/signin.html',
         'authentication_form': SigninForm}, name='signin'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/accounts/signin/'}, name='auth_logout'),
    url(r'^accounts/signup/$', RegistrationView.as_view(
        template_name='registration/signup.html',
        form_class=SignupForm), name='signup'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', admin.site.urls),
]
