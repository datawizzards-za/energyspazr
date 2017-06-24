# Django
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

# Crispy forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Div, Field, Button

# Local Django
from app import models


class SigninForm(auth_forms.AuthenticationForm):

    class Meta(auth_forms.AuthenticationForm):
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


class SignupForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email']

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
            css_class='form-group'
        )
    )


class UserAccountUpdateForm(ModelForm):
    building_name = forms.CharField(max_length=30)
    street_name = forms.CharField(max_length=30)
    province = forms.ChoiceField(choices=(), required=True)
    roles = forms.ChoiceField(choices=(), required=True)
    city = forms.CharField(max_length=30)
    suburb = forms.CharField(max_length=30)
    zip_code = forms.IntegerField()

    def __init__(self, p_choices, r_choices, *args, **kwargs):
        super(UserAccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['province'].choices = p_choices
        self.fields['roles'].choices = r_choices

    class Meta:
        model = models.SpazrUser
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
                      placeholder='Compay Name'), css_class='col-md-6'
            ),
            Div(
                Field('company_reg', css_class='form-control text-center ',
                      placeholder='Company Reg. Number'), css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('contact_number', css_class='form-control text-center ',
                      placeholder='Contact Number'), css_class='col-md-6'
            ),
            Div(
                Field('web_address', css_class='form-control text-center ',
                      placeholder='Web Address'), css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('roles', css_class='form-control text-center ',
                      placeholder='Role(s)'), css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        HTML('<h5 class="text-center">Physical Address</h5><hr>'),
        Div(
            Div(
                Field('building_name', css_class='form-control text-center ',
                      placeholder='Building Name'), css_class='col-md-6'
            ),
            Div(
                Field('street_name', css_class='form-control text-center ',
                      placeholder='Street Name'), css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('province', css_class='form-control text-center ',
                      placeholder='Provice'), css_class='col-md-6 text-center'
            ),
            Div(
                Field('city', css_class='form-control text-center ',
                      placeholder='City'), css_class='col-md-6 '
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('suburb', css_class='form-control text-center ',
                      placeholder='Suburb'), css_class='col-md-6'
            ),
            Div(
                Field('zip_code', css_class='form-control text-center ',
                      placeholder='ZIP Code'), css_class='col-md-6'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                HTML(""),
                css_class='col-md-4'
            ),
            Div(
                FormActions(Submit('login', 'PROCEED',
                                   css_class='btn btn-primary btn-block')),
                css_class='col-md-4'
            ),
            css_class='card-footer'
        ),
    )


class PVTOrderForm(ModelForm):
    property_type = forms.ChoiceField(choices=(['flat', 'FLAT'],
                                               ['house', 'HOUSE']))
    roof_inclination = forms.ChoiceField(choices=(['tilted', 'TILTED'],
                                                  ['flat', 'FLAT']))
    need_finance = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    include_installation = forms.ChoiceField(choices=(['yes', 'YES'],
                                                      ['no', 'NO']))

    intended_use = forms.ChoiceField(choices=(['main_power', 'MAIN POWER'],
                                              ['backup_power', 'BACK UP']))
    site_visit = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    OPTIONS = ((p.name, p.name) for p in models.Appliance.objects.all())
    name = forms.ChoiceField(choices=OPTIONS, required=True)
    username = forms.CharField(max_length=1000)
    physical_address = forms.CharField(max_length=1000)
    contact_number = forms.CharField(max_length=1000)
    last_name = forms.CharField(max_length=1000)
    first_name = forms.CharField(max_length=1000)

    class Meta:
        model = models.Appliance
        fields = ['name']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False
    helper.layout = Layout(
        Div(
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
                    Field('roof_inclination',
                          css_class='form-control text-center',
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
            Which of these appliances you want to power? \
            </label>"),
                Div(
                    Field('name',
                          css_class='form-control selectpicker text-center',
                          multiple='true',
                          placeholder='Select multiple appliances',
                          data_done_button='true', id='done'),
                    css_class='col-md-5 text-center'
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
                css_class='form-group form-horizontal'
            ),
            Div(
                Div(
                    HTML(""),
                    css_class='col-md-2'
                ),
                Div(
                    HTML("<a class='btn btn-warning btn-block icon-btn' \
                 href='{% url 'our_products' %}'> Cancel</a>"),
                    css_class='col-md-4'
                ),
                Div(
                    FormActions(Button('login', 'PROCEED',
                                       css_class='btn btn-primary btn-block',
                                       data_target="#targetElement",
                                       data_toggle="collapse",
                                       css_id='proceed'
                                       )
                                ),
                    css_class='col-md-4'
                ),
                css_class='card-footer'
            ),
            css_id='targetElement',
            css_class='card login-box long'
        ),
        Div(
            HTML(
                "<h3 class ='login-head'>Let's complete your order.</h3>"),
            Div(
                Div(
                    Div(
                        Div(
                            Field('first_name',
                                  css_class='form-control text-center form-control'
                                  , placeholder='First Name',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                Div(
                    Div(
                        Div(
                            Field('last_name',
                                  css_class='form-control text-center form-control'
                                  , placeholder='Last Name',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                css_class='row mb-20',
            ),
            Div(
                Div(
                    Div(
                        Div(
                            Field('username',
                                  css_class='form-control emailinput text-center form-control'
                                  , placeholder='Email Address',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                Div(
                    Div(
                        Div(
                            Field('contact_number',
                                  css_class='form-control text-center form-control'
                                  , placeholder='Contact Number',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                css_class='row mb-20',
            ),
            Div(
                Div(
                    Div(
                        Field('physical_address',
                              css_class='form-control text-center textinput textInput '
                                        'form-control',
                              placeholder='Delivery address',
                              required='true'),
                        css_class='controls'
                    ),
                    css_class='form-group'
                ),
                css_class='col-md-12'
            ),
            Div(
                Div(
                    css_class='form-group col-md-3'
                ),
                Div(
                    Div(
                        Submit('place_order', 'FINISH',
                               css_class='btn btn-primary btn btn-primary btn-block'
                               ),
                        css_class='controls'
                    ),
                    css_class='form-group col-md-6'
                ),
                css_class='form-group btn-container'
            ),

            css_class='card login-box finish_order'
        )

    )


class GeyserOrderForm(forms.Form):
    property_type = forms.ChoiceField(
        choices=(['flat', 'FLAT'], ['house', 'HOUSE']))
    roof_inclination = forms.ChoiceField(
        choices=(['tilted', 'TILTED'], ['flat', 'FLAT']))
    # new_system = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    existing_geyser = forms.ChoiceField(choices=([False, 'NO'],
                                                 [True, 'YES']))

    water_collector = forms.ChoiceField(choices=(['flat_plate', 'FLAT PLATE'],
                                                 ['evacuated_tubes',
                                                  'EVACUATED TUBES']))
    current_geyser_size = forms.CharField(max_length=1000)
    users_number = forms.CharField(max_length=1000)
    required_geyser_size = forms.ChoiceField(
        choices=(['same_size', 'SAME AS CURRENT'],
                 ['recommended', 'X (RECOMMENDED)'],
                 ['100_liters', '100L'],
                 ['150_liters', '150L'],
                 ['200_liters', '200L']))
    # same_as_existing = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    need_finance = forms.ChoiceField(choices=(['yes', 'YES'], ['no', 'NO']))
    include_installation = forms.ChoiceField(
        choices=(['yes', 'YES'], ['no', 'NO']))

    username = forms.CharField(max_length=1000)
    physical_address = forms.CharField(max_length=1000)
    contact_number = forms.CharField(max_length=1000)
    last_name = forms.CharField(max_length=1000)
    first_name = forms.CharField(max_length=1000)

    class Meta:
        model = models.GeyserSystemOrder
        fields = ['property_type', 'roof_inclination', 'existing_geyser',
                  'current_geyser_size', 'users_number',
                  'required_geyser_size']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
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
                    Field('roof_inclination',
                          css_class='form-control text-center',
                          placeholder='Select Roof'),
                    css_class='col-md-5 text-center'
                ),
                css_class='form-group form-horizontal'
            ),
            Div(
                HTML("<label class='control-label col-md-7'> \
                 Preferred water collector\
                </label>"),
                Div(
                    Field('water_collector',
                          css_class='form-control text-center'),
                          css_class='col-md-5 text-center'
                ),
                css_class='form-group form-horizontal'
            ),
            Div(
                HTML("<label class='control-label col-md-7'> \
                Number of people using geyser \
                </label>"),
                Div(
                    Field('users_number', css_class='form-control'),
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
                Size of current geyser \
                </label>"),
                Div(
                    Field('current_geyser_size', css_class='form-control'),
                    css_class='col-md-5 text-center'
                ),
                css_class='form-group form-horizontal'
            ),
            Div(
                HTML("<label class='control-label col-md-7'> \
                Required geyser size \
                </label>"),
                Div(
                    Field('required_geyser_size', css_class='form-control'),
                    css_class='col-md-5 text-center'
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
                    Field('need_finance', css_class='form-control'),
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
                    FormActions(Button('login', 'PROCEED',
                                       css_class='btn btn-primary btn-block',
                                       data_target="#targetElement",
                                       data_toggle="collapse",
                                       css_id='proceed'
                                       )
                                ),
                    css_class='col-md-4'
                ),
                css_class='card-footer'
            ),

            css_id = 'targetElement',
            css_class = 'card login-box vlong'

        ),
        Div(
            HTML(
                "<h3 class ='login-head'>Let's complete your order.</h3>"),
            Div(
                Div(
                    Div(
                        Div(
                            Field('first_name',
                                  css_class='form-control text-center form-control'
                                  , placeholder='First Name',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                Div(
                    Div(
                        Div(
                            Field('last_name',
                                  css_class='form-control text-center form-control'
                                  , placeholder='Last Name',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                css_class='row mb-20',
            ),
            Div(
                Div(
                    Div(
                        Div(
                            Field('username',
                                  css_class='form-control emailinput text-center form-control'
                                  , placeholder='Email Address',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                Div(
                    Div(
                        Div(
                            Field('contact_number',
                                  css_class='form-control text-center form-control'
                                  , placeholder='Contact Number',
                                  type='text',
                                  maxlength='30'
                                  ),
                            css_class='controls'),
                        css_class='form-group'
                    ),
                    css_class='col-md-6'
                ),
                css_class='row mb-20',
            ),
            Div(
                Div(
                    Div(
                        Field('physical_address',
                              css_class='form-control text-center textinput textInput '
                                        'form-control',
                              placeholder='Delivery address',
                              required='true'),
                        css_class='controls'
                    ),
                    css_class='form-group'
                ),
                css_class='col-md-12'
            ),
            Div(
                Div(
                    css_class='form-group col-md-3'
                ),
                Div(
                    Div(
                        Submit('place_order', 'FINISH',
                               css_class='btn btn-primary btn btn-primary btn-block'
                               ),
                        css_class='controls'
                    ),
                    css_class='form-group col-md-6'
                ),
                css_class='form-group btn-container'
            ),

            css_class='card login-box finish_order'
        ),
    )


class ResendForm(forms.Form):
    email = forms.CharField(max_length=1000)


class AddComponentForm(forms.Form):
    COMPOS = (['solar_panel', 'SOLAR PANEL'],
              ['solar_battery', 'SOLAR BATTERY'])
    components = forms.ChoiceField(choices=COMPOS, required=True)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Div(
                Field('components',
                      css_class='form-control selectpicker text-center',
                      multiple='true', data_done_button='true', id='done'),
                css_class='col-md-12'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                HTML("<a class='btn btn-warning btn-block icon-btn' \
                 href='{% url 'component-order' %}'> Cancel</a>"),
                css_class='col-md-6'
            ),
            Div(
                FormActions(Submit('okay', 'Okay',
                                   css_class='btn btn-primary btn-block')),
                css_class='form-group col-md-6'
            ),
            css_class='card-footer col-md-12'
        ),
    )


class EditProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.FloatField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Div(
                Field('name', 
                      id='edit_prod_name',
                      placeholder='Product name',
                      css_class='form-control text-center'),
                css_class='col-md-12 text-center'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('price',
                      id='edit_prod_price',
                      placeholder='Product price, e.g., R100.50',
                      css_class='form-control text-center'),
                css_class='col-md-12 text-center'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                HTML("<a class='btn btn-warning btn-block icon-btn' \
                 href='{% url 'my-products' %}'> Cancel</a>"),
                css_class='col-md-6'
            ),
            Div(
                FormActions(Submit('okay', 'Okay',
                                   css_class='btn btn-primary btn-block')),
                css_class='form-group col-md-6'
            ),
            css_class='card-footer col-md-12'
        ),
    )


class NewProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.FloatField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Div(
                Field('name',
                      id='new_prod_name',
                      placeholder='Product name',
                      css_class='form-control text-center'),
                css_class='col-md-12 text-center'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                Field('price',
                      id='new_price_name',
                      placeholder='Product price, e.g., R100.50',
                      css_class='form-control text-center'),
                css_class='col-md-12 text-center'
            ),
            css_class='row mb-20'
        ),
        Div(
            Div(
                HTML("<a class='btn btn-warning btn-block icon-btn' \
                 href='{% url 'my-products' %}'> Cancel</a>"),
                css_class='col-md-6'
            ),
            Div(
                FormActions(Submit('okay', 'Okay',
                                   css_class='btn btn-primary btn-block')),
                css_class='form-group col-md-6'
            ),
            css_class='card-footer col-md-12'
        ),
    )
