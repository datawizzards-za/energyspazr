from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Div, Field
from crispy_forms.bootstrap import FormActions
from django import forms

class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta(AuthenticationForm):
        model = User

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'login-form'
    helper.form_show_labels = False
    helper.layout = Layout(
        HTML('<h3 class="login-head"><i class="fa fa-lg fa-fw fa-user">'\
            '</i>SIGN IN</h3>'),
        Div(
            HTML('<label class="control-label">USERNAME</label>'),
            Field('username', css_class='form-control', autofocus=True),
            css_class='form-group'
        ),
        Div(
            HTML('<label class="control-label">PASSWORD</label>'),
             Field('password', css_class='form-control'),
            css_class='form-group'
        ),
        Div(
            Div(
                Div(
                    HTML('<label class="semibold-text">'\
                        '<input type="checkbox">'\
                        '<span class="label-text">'\
                        'Stay Signed in</span></label>'),
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
        )
    )


class RegistrationForm(UserCreationForm):
    password1 = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['username', 'password','email',
                  'first_name', 'last_name']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'login-form'
    helper.form_show_labels = False

    helper.layout = Layout(
        HTML('<h3 class="login-head"><i class="fa fa-lg fa-fw fa-user">' \
             '</i>SIGN UP</h3>'),
        Div(
            Div(
                Field('first_name', css_class='form-control', placeholder='First Name', autofocus=True),
                css_class='col-md-4'
            ),
            Div(
                Field('last_name', css_class='form-control', placeholder='Last Name'),
                css_class='col-md-4'
            ),
            css_class='row mb-20'
        ),
        Div(
            HTML('<label class="control-label">PASSWORD</label>'),
            Field('password', css_class='form-control'),
            css_class='form-group'
        ),
        Div(
            Div(
                Div(
                    HTML('<label class="semibold-text">' \
                         '<input type="checkbox">' \
                         '<span class="label-text">' \
                         'Stay Signed in</span></label>'),
                    css_class='animated-checkbox'
                ),
                HTML('<p class="semibold-text mb-0">' \
                     '<a data-toggle="flip">Forgot Password ?</a></p>'),
                css_class='utility'
            ),
            css_class='form-group'
        ),
        Div(
            FormActions(Submit('login', 'SIGN IN',
                               css_class='btn btn-primary btn-block')),
            css_class='form-group btn-container'
        )
    )
