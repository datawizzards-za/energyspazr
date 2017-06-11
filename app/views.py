from django.shortcuts import render, HttpResponseRedirect, HttpResponse, \
    reverse, redirect
from django.views import View
from app.forms import FinancierUpdateAccountForm, UserRoleForm
from app.models import Financier, PhysicalAddress, UserRole
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import User
from registration.backends.hmac.views import ActivationView

# Create your views here.
class Dashboard(LoginRequiredMixin, View):
    template_name = 'app/index.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)


class Home(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)


class ActivateUser(ActivationView):
    
    def activate(self, *args, **kwargs):
        user =  super(ActivateUser, self).activate(*args, **kwargs)
        if user:
            print "Authenticated: ", user.is_authenticated
        return user

    def get_success_url(self, user):
        return ('user_roles', (), {})


class FinancierUpdateAccount(View):
    template_name = 'registration/financier_update_account.html'
    form_class = FinancierUpdateAccountForm
    address_model_class = PhysicalAddress

    def post(self, request, *args, **kwargs):
        """

        """
        form = self.form_class()
        if form.is_valid():
            address_model = self.address_model_class(request)

            user = request.user
            company_name = form.cleaned_data['company_name']
            company_reg = form.cleaned_data['company_reg']
            contact_number = form.cleaned_data['contact_number']
            web_address = form.cleaned_data['web_address']
            physical_address = address_model.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=form.cleaned_data['province'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            Financier.objects.create(
                user=user,
                company_name=company_name,
                company_reg=company_reg,
                contact_number=contact_number,
                web_address=web_address,
                physical_address=physical_address)
            
        return render(request , self.template_name)
        
    def get(self, request, *args, **kwargs):
    
        """
        """
        
        form = self.form_class()

        context = {'form':form}
        
        return render(request, self.template_name, context)


class UserRoleView(View):

    template_name = 'app/user_roles_form.html'
    form_class = UserRoleForm
    model_class = UserRole

    def get(self, request, *args, **kwargs):
        """
        """
        form = self.form_class(self.get_form_choices())
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.get_form_choices(), request.POST)

        if form.is_valid():
            user = request.user
            print "User: ", user
            role_id = int(form.cleaned_data['role'])
            print "ROLE_ID: ", role_id
            role = self.model_class.objects.filter(pk=role_id)[0]
            print role
            user.role = role
            user.save()
            return redirect(reverse('financier'))

        context = {'form':form}
        return render(request, self.template_name, context)

    def get_form_choices(self):
        roles = self.model_class.objects.all()

        return tuple([[role.pk, role.name] for role in roles])


class OurProducts(View):
    template_name = 'home/products.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)


class PVT(View):
    template_name = 'home/pvt.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)

class SolarGeyser(View):
    template_name = 'home/geyser.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)


class SolarComponent(View):
    template_name = 'home/component.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)

class Register(View):
    template_name = 'home/register.html'

    def get(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name)
