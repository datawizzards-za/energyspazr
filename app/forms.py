from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Div, Field
from crispy_forms.bootstrap import FormActions

from app.models import Financier, Appliance, SupplierInstaller, GeyserSystemOrder

class SigninForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = User
        fields = ['username', 'password']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'login-form'
    helper.form_show_labels = False
    helper.layout = Layout(
        HTML('<h3 class="login-head"><i class="fa fa-lg fa-fw fa-user">' \
             '</i>SIGN IN</h3>'),
        Div(
            Field('username', css_class='form-control text-center',
                  placeholder='Email Address', autofocus=True),
            css_class='form-group'
        ),
        Div(
            Field('password', placeholder='Password',
                  css_class='form-control text-center'),
            css_class='form-group'
        ),
        Div(
            Div(
                Div(
                    HTML('<label class="semibold-text">' \
                         '<input type="checkbox"></label>'),
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
        ),
        Div(
            Div(
                HTML('<br /><p class="semibold-text mb-0">' \
                     "<a href='{% url 'signup' %}'>Not Registered?</a></p>")
            ),
            css_class='form-group text-center'
        )
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

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
                Field('email', css_class='form-control text-center',
                      placeholder='Email Address'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('password1', css_class='form-control text-center ',
                      placeholder='Password'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('password2', css_class='form-control text-center ',
                      placeholder='Confirm Password'),
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
            css_class='form-group')
    )


class FinancierUpdateAccountForm(ModelForm):
    def __init__(self, provinces_choices, *args, **kwargs):
        super(FinancierUpdateAccountForm, self).__init__(*args, **kwargs)
        self.fields['province'].choices = provinces_choices

    building_name = forms.CharField(max_length=30)
    street_name = forms.CharField(max_length=30)
    province = forms.ChoiceField(choices=(), required=True)
    city = forms.CharField(max_length=30)
    suburb = forms.CharField(max_length=30)
    zip_code = forms.IntegerField()

    class Meta:
        model = Financier
        fields = ['company_name', 'company_reg', 'contact_number',
                  'web_address']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        HTML('<h3 class="login-head">ACCOUNT DETAILS</h3>'),
        Div(
            Div(
                Field('company_name', css_class='form-control text-center',
                      placeholder='Compay Name'),
                css_class='col-md-6'
            ),
            Div(
                Field('company_reg', css_class='form-control text-center ',
                      placeholder='Company Reg. Number'),
                css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('contact_number', css_class='form-control text-center ',
                      placeholder='Contact Number'),
                css_class='col-md-6'
            ),
            Div(
                Field('web_address', css_class='form-control text-center ',
                      placeholder='Web Address'),
                css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        HTML('<h5 class="text-center">Physical Address</h5><hr>'),
        Div(
            Div(
                Field('building_name', css_class='form-control text-center ',
                      placeholder='Building Name'),
                css_class='col-md-6'
            ),
            Div(
                Field('street_name', css_class='form-control text-center ',
                      placeholder='Street Name'),
                css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('province', css_class='form-control text-center ',
                      placeholder='Provice'),
                css_class='col-md-6'
            ),
            Div(
                Field('city', css_class='form-control text-center ',
                      placeholder='City'),
                css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('suburb', css_class='form-control text-center ',
                      placeholder='Suburb'),
                css_class='col-md-6'
            ),
            Div(
                Field('zip_code', css_class='form-control text-center ',
                      placeholder='ZIP Code'),
                css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            FormActions(Submit('login', 'PROCEED',
                               css_class='btn btn-primary btn-block')),
            css_class='form-group btn-container'
        ),
        Div(
            Div(
                HTML('<br /><p class="semibold-text mb-0 text-center">' \
                     "<a href='{% url 'home' %}'>Cancel Registration Process</a></p>")
            ),
            css_class='form-group'
        )
    )



class PVTOrderForm(ModelForm):
    TYPES = (
        ('H', 'Home'),
        ('R', 'Rental')
    )
    property_type = forms.ChoiceField(choices=TYPES, required=True)
    roof_inclination = forms.CharField(max_length=30)
    intended_use = forms.CharField(max_length=30)
    site_visit = forms.CharField(max_length=30)
    OPTIONS = ((p.pk, p.name) for p in Appliance.objects.all())
    name = forms.ChoiceField(choices=OPTIONS, required=True)

    class Meta:
        model = Appliance
        fields = ['name']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False
    helper.layout = Layout(
        HTML('<h3 class="login-head">PVT SYSTEM</h3>'),
        Div(
            HTML("<label class='control-label col-md-7'> \
            What type of property do you have?</label>"),
            Div(
                Field('property_type', css_class='form-control',
                      placeholder='Type of Property'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
        ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            What is the inclination of your roof? \
            </label>"),
            Div(
                Field('roof_inclination', css_class='form-control text-center',
                      placeholder='Select Roof'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
        ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            What do you intend to use this sytem for? \
            </label>"),
            Div(
                Field('intended_use', css_class='form-control',
                      placeholder='Type of Property'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Would you like to arrange a site visit? \
            </label>"),
            Div(
                Field('site_visit', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Which of these appliances you want to power \
            </label>"),
            Div(
                Field('possible_appliances', css_class='form-control text-center',
                      placeholder='Select multiple appliances'),
                css_class='col-md-5'
                ),
            css_class='form-group form-horizontal'),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Include installation costs? \
            </label>"),
            Div(
                Field('include_installation', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Apply for finance? \
            </label>"),
            Div(
                Field('need_finance', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'),
        Div(
            Div(
                HTML(""),
                css_class='col-md-4'
                ),
            Div(
                HTML("<a class='btn btn-default btn-block icon-btn' \
                 href='{% url 'our_products' %}'> Cancel</a>"),
                css_class='col-md-4'
                ),
            Div(
                FormActions(Submit('login', 'PROCEED', css_class='btn btn-primary btn-block')),
                css_class='col-md-4'
                ),
            css_class='card-footer'
        ),
    )
    
    
class GeyserOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pass
    
    property_type = forms.ChoiceField(choices=(['flat', 'FLAT'], ['house', 'HOUSE']))
    roof_inclination = forms.ChoiceField(choices=(['tilted', 'TILTED'], ['flat', 'FLAT']))
    #new_system = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    existing_geyser = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    water_collector = forms.ChoiceField(choices=())
    current_geyser_size = forms.ChoiceField(choices=(['main_power', 'MAIN POWER'],
                                                     ['backup_power', 'BACK UP']))
    users_number = forms.CharField(max_length=1000)
    required_geyser_size = forms.ChoiceField(choices=(['same_size', 'SAME AS CURRENT'],
                                                      ['recommended', 'X (RECOMMENDED)'],
                                                      ['recommended', 'X (RECOMMENDED)'],
                                                      ['100_liters', '100L'],
                                                      ['150_liters', '150L'],
                                                      ['200_liters', '200L']))
    #same_as_existing = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    need_finance = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    include_installation = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))

    class Meta(GeyserSystemOrder):
        model = GeyserSystemOrder
        fields = ['property_type', 'roof_inclination', 'existing_geyser',
                  'current_geyser_size', 'users_number', 'required_geyser_size']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        HTML('<h3 class="login-head">SOLAR GEYSER</h3>'),
        Div(
            HTML("<label class='control-label col-md-7'> \
            What type of property do you have?</label>"),
            Div(
                Field('property_type', css_class='form-control',
                      placeholder='Type of Property'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
        ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            What is the inclination of your roof? \
            </label>"),
            Div(
                Field('roof_inclination', css_class='form-control text-center',
                      placeholder='Select Roof'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
        ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Do you currently have a geyser? \
            </label>"),
            Div(
                Field('existing_geyser', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            ? \
            </label>"),
            Div(
                Field('existing_geyser', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Which of these appliances you want to power \
            </label>"),
            Div(
                Field('possible_appliances', css_class='form-control text-center',
                      placeholder='Select multiple appliances'),
                css_class='col-md-5'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Include installation costs? \
            </label>"),
            Div(
                Field('include_installation', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            HTML("<label class='control-label col-md-7'> \
            Apply for finance? \
            </label>"),
            Div(
                Field('apply_finance', css_class='form-control'),
                css_class='col-md-5 text-center'
                ),
            css_class='form-group form-horizontal'
            ),
        Div(
            Div(
                HTML(""),
                css_class='col-md-4'
                ),
            Div(
                HTML("<a class='btn btn-default btn-block icon-btn' \
                 href='{% url 'our-products' %}'> Cancel</a>"),
                css_class='col-md-4'
                ),
            Div(
                FormActions(Submit('login', 'PROCEED', css_class='btn btn-primary btn-block')),
                css_class='col-md-4'
                ),
            css_class='card-footer'
        ),
    )


class UserRoleForm(forms.Form):
    def __init__(self, role_choices, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = role_choices

    role = forms.ChoiceField(choices=(), required=True)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_id = 'role_form'
    helper.layout = Layout(
        'role',
        Div(
            FormActions(Submit('proceed', 'PROCEED',
                               css_class='btn btn-primary btn-block')),
            css_class='form-group btn-container'),
        )
