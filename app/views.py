# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views import View

# Other Libraries
from registration.backends.hmac.views import ActivationView

# Local Django
from app import forms
from app import models
from app.utils import quatation_pdf


class Dashboard(LoginRequiredMixin, View):
    template_name = 'app/supplier/dashboard.html'

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
    """
    """

    def get_success_url(self, user):
        return ('user_roles', (), {})


class FinancierUpdateAccount(LoginRequiredMixin, View):
    template_name = 'registration/financier_update_account.html'
    form_class = forms.FinancierUpdateAccountForm
    address_model_class = models.PhysicalAddress
    financier_model_class = models.Financier

    def get(self, request, *args, **kwargs):
        """
        """
        form = self.form_class(self.provinces_choices())
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        form = self.form_class(self.provinces_choices(), request.POST)
        if form.is_valid():
            address_model = self.address_model_class(request)

            user = request.user
            company_name = form.cleaned_data['company_name']
            company_reg = form.cleaned_data['company_reg']
            contact_number = form.cleaned_data['contact_number']
            web_address = form.cleaned_data['web_address']
            province_id = form.cleaned_data['province']
            province = models.Province.objects.filter(pk=province_id)[0]
            physical_address = self.address_model_class.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            self.financier_model_class.objects.create(
                user=user,
                company_name=company_name,
                company_reg=company_reg,
                contact_number=contact_number,
                web_address=web_address,
                physical_address=physical_address)

            return redirect(reverse('dashboard'))

        form = self.form_class(self.provinces_choices())
        context = {'form': form}

        return render(request, self.template_name, context)

    def provinces_choices(self):
        provinces = models.Province.objects.all()
        return tuple([[p.pk, p.name] for p in provinces])


class SupplierInstallerUpdateAccount(LoginRequiredMixin, View):
    template_name = 'registration/financier_update_account.html'
    form_class = forms.FinancierUpdateAccountForm
    address_model_class = models.PhysicalAddress
    supplier_install_model_class = models.SupplierInstaller

    def get(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices()
        form = self.form_class(p_choices)
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices()
        form = self.form_class(p_choices, request.POST)

        if form.is_valid():
            address_model = self.address_model_class(request)

            user = request.user
            company_name = form.cleaned_data['company_name']
            company_reg = form.cleaned_data['company_reg']
            contact_number = form.cleaned_data['contact_number']
            web_address = form.cleaned_data['web_address']
            province_id = form.cleaned_data['province']
            province = models.Province.objects.filter(pk=province_id)[0]
            physical_address = self.address_model_class.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            self.supplier_install_model_class.objects.create(
                user=user,
                company_name=company_name,
                company_reg=company_reg,
                contact_number=contact_number,
                web_address=web_address,
                physical_address=physical_address)

            return redirect(reverse('dashboard'))

        form = self.form_class(self.provinces_choices())
        context = {'form': form}

        return render(request, self.template_name, context)

    def provinces_choices(self):
        provinces = models.Province.objects.all()
        return ([[p.pk, p.name] for p in provinces])


class UserRoleView(LoginRequiredMixin, View):
    template_name = 'app/user_roles_form.html'
    form_class = forms.UserRoleForm
    model_class = models.UserRole

    def get(self, request, *args, **kwargs):
        """
        """
        form = self.form_class(self.get_form_choices())
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.get_form_choices(), request.POST)

        if form.is_valid():
            user = request.user
            role_id = int(form.cleaned_data['role'])
            role = self.model_class.objects.filter(pk=role_id)[0]
            user.role = role
            user.save()

            if role.name == 'Financier':
                return redirect(reverse('financier'))
            elif role.name == 'Installer' or role.name == 'Supplier':
                return redirect(reverse('supplier_installer'))
            else:
                return redirect(reverse('dashboard'))

        context = {'form': form}
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
    template_name = 'app/component_order.html'

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


class ClientOrder(View):
    template_name = 'app/client_order.html'
    """
    address_model_class = PhysicalAddress

    def post(self, request, *args, **kwargs):
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
        """

    def get(self, request, *args, **kwargs):
        """
        """
        return render(request, self.template_name)


class OrderPVTSystem(View):
    template_name = 'app/pvt_order.html'
    appliances_model_class = models.Appliance
    form_class = forms.PVTOrderForm

    def get(self, request, *args, **kwargs):
        """
        """
        form = self.form_class()
        print form.data
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        form = self.form_class(request.POST)
        print form.data
        if form.is_valid():
            appliances_model = self.appliances_model_class(request.POST)

            # user = request.user
            intended_use = form.cleaned_data['intended_use']
            site_visit = bool(form.cleaned_data['site_visit'])
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            # print (form.cleaned_data['name'])
            # possible_appliances = Appliance(name=form.cleaned_data['name'])
            # possible_appliances.save()
            #
            # pvt_system = PVTSystem(
            #     roof_inclination=roof_inclination,
            #     property_type=property_type,
            #     site_visit=site_visit,
            #     intended_use=intended_use)
            #
            # pvt_system.save()
            # pvt_system.possible_appliances.add(possible_appliances)
            quatation_pdf.generate_pdf(form.data)
        return redirect('/app/client-info/')

    def appliances_choices(self):
        appliance = Appliance.objects.all()
        return tuple([[p.pk, p.name] for p in appliance])


class OrderGeyser(View):
    template_name = 'app/geyser_order.html'
    form_class = forms.GeyserOrderForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    """ 
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.appliance_choices(), request.POST)
        if form.is_valid():
            user = request.user
            intended_use = form.cleaned_data['intended_use']
            site_visit = form.cleaned_data['site_visit']
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            
            pvt_system = PVTSystem.objects.create(
                roof_inclination=roof_inclination,
                property_type=property_type,
                site_visit=site_visit,
                intended_use=intended_use)
            
            possible_appliances = form.cleaned_data['possible_appliances']
            for appliance in possible_appliances:
                this_appliance = appliance.objects.filter(pk=appliance)[0]
                pvt_system.possible_appliances.add(this_appliance)
                pvt_system.save()

        return render(request , self.template_name) """


class DisplayPDF(View):

    def get(self, request):
        image_data = open("app/static/app/slips/MabuManailengSat Jun 17 "
                          "22:15:20 2017.pdf", "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")


class AddComponent(View):    
    template_name = 'app/add_component.html'
    form_class = forms.AddComponentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form':form}
        return render(request, self.template_name, context)

    """ 
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.appliance_choices(), request.POST)
        if form.is_valid():
            user = request.user
            intended_use = form.cleaned_data['intended_use']
            site_visit = form.cleaned_data['site_visit']
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            
            pvt_system = PVTSystem.objects.create(
                roof_inclination=roof_inclination,
                property_type=property_type,
                site_visit=site_visit,
                intended_use=intended_use)
            
            possible_appliances = form.cleaned_data['possible_appliances']
            for appliance in possible_appliances:
                this_appliance = appliance.objects.filter(pk=appliance)[0]
                pvt_system.possible_appliances.add(this_appliance)
                pvt_system.save()

        return render(request , self.template_name) """


class MyProducts(LoginRequiredMixin, View):

    template_name = 'app/supplier/products.html'

    def get(self, request, *args, **kwargs):
        """
        """
        return render(request, self.template_name)