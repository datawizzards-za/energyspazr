from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Div, Field
from crispy_forms.bootstrap import FormActions
from django import forms

class SigninForm(AuthenticationForm):
    
    class Meta(AuthenticationForm):
        model = User
        fields = ['username', 'password']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'login-form'
    helper.form_show_labels = False
    helper.layout = Layout(
        HTML('<h3 class="login-head"><i class="fa fa-lg fa-fw fa-user">'\
            '</i>SIGN IN</h3>'),
        Div(
            Field('username', css_class='form-control text-center',
                  placeholder='Email Address', autofocus=True),
            css_class='form-group'
        ),
        Div(
             Field('password', placeholder='Password', css_class='form-control text-center'),
            css_class='form-group'
        ),
        Div(
            Div(
                Div(
                    HTML('<label class="semibold-text">'\
                        '<input type="checkbox"></label>'),
                    css_class='animated-checkbox'
                ),
                HTML('<p class="semibold-text mb-0">'\
                    '<a data-toggle="flip">Forgot Password ?</a></p>'),
                css_class='utility'
            ),
            css_class='form-group'
        ),
        Div(
            FormActions(Submit('login', 'SIGN IN',
                                   css_class='btn btn-primary btn-block')),
            css_class='form-group btn-container'
        ),
        Div(
            Div(
                HTML('<br /><p class="semibold-text mb-0">' \
                     "<a href='{% url 'signup' %}'>Already Registered?</a></p>")
            ),
            css_class='form-group text-center'
        )
    )


class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        HTML('<h3 class="login-head"><i class="fa fa-lg fa-fw fa-user">' \
             '</i>SIGN UP</h3>'),
        Div(
            Div(
                Field('username', css_class='form-control text-center',
                      placeholder='Username'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('first_name', css_class='form-control text-center', placeholder='First Name', autofocus=True),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('last_name', css_class='form-control text-center', placeholder='Last Name'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('email', css_class='form-control text-center', placeholder='Email Address'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('password1', css_class='form-control text-center ', placeholder='Password'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('password2', css_class='form-control text-center ', placeholder='Confirm Password'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            FormActions(Submit('signup', 'SIGN UP',
                               css_class='btn btn-primary btn-block')),
            css_class='form-group btn-container'
        ),
        Div(
            Div(
                HTML('<br /><p class="semibold-text mb-0 text-center">' \
                     "<a href='{% url 'signin' %}'>Already Registered?</a></p>")
            ),
            css_class='form-group'
        )
    )
