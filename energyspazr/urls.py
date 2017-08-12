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
from django.urls import reverse, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views

from registration.backends.hmac.views import RegistrationView

from app import forms
from app import views

urlpatterns = [
    url(r'^\Z', include('app.urls')),
    url(r'^app/', include('app.urls')),

    url(r'^accounts/signin/$', auth_views.login,
        {'template_name': 'registration/signin.html',
         'authentication_form': forms.SigninForm,
         'redirect_authenticated_user': True}, name='signin'),

    url(r'^accounts/signup/$', RegistrationView.as_view(
        template_name='registration/signup.html',
        form_class=forms.SignupForm), name='signup'),

    url(r'^accounts/resend/$', RegistrationView.as_view(
        template_name='registration/resend_activation_form.html',
        form_class=forms.ResendForm), name='resend'),

    url(r'^accounts/forgot-password/$',
        auth_views.PasswordResetView.as_view(
            template_name='registration/forgot_pass.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('pass-reset-send'),
            form_class=forms.ForgotPassForm), name='forgot-pass'),
    url(r'^accounts/password-reset-send/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/pass_reset_send.html'), name='pass-reset-send'),
    url(r'^accounts/set-password/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/set_pass.html',
            success_url=reverse_lazy('reset-pass-done'),
            form_class=forms.SetPasswordForm), name='set-pass'),
    url(r'^accounts/reset-password-complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/reset_pass_done.html'), name='reset-pass-done'),

    url(r'^accounts/activate/(?P<activation_key>[-:\w]+)/$',
        views.ActivateUser.as_view(), name='registration_activate'),

    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]
