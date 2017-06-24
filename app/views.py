# Django
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views import View

# Other Libraries
from registration.backends.hmac.views import ActivationView

# Local Django
from app import forms
from app import models
from app.utils import quotation_pdf


class Dashboard(LoginRequiredMixin, View):
    template_name = 'app/supplier/dashboard.html'
    user_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        user = self.user_model_class.objects.filter(user=req_user)[0]
        context = {'user': user}

        return render(request, self.template_name, context)


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
        login(self.request, user)
        return ('user_account_update', (), {})


class UserAccountUpdate(LoginRequiredMixin, View):
    template_name = 'registration/financier_update_account.html'
    form_class = forms.UserAccountUpdateForm
    address_model_class = models.PhysicalAddress
    user_model_class = models.SpazrUser
    province_model_class = models.Province

    def get(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices
        r_choices = self.roles_choices
        form = self.form_class(p_choices, r_choices)
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices
        r_choices = self.roles_choices
        form = self.form_class(p_choices, r_choices, request.POST)

        if form.is_valid():
            address_model = self.address_model_class(request)

            user = request.user
            group_id = int(form.cleaned_data['roles'])
            group = Group.objects.filter(pk=group_id)[0]
            user.groups.add(group)

            company_name = form.cleaned_data['company_name']
            company_reg = form.cleaned_data['company_reg']
            contact_number = form.cleaned_data['contact_number']
            web_address = form.cleaned_data['web_address']
            province_id = form.cleaned_data['province']
            province = \
                self.province_model_class.objects.filter(pk=province_id)[0]

            physical_address = self.address_model_class.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            self.user_model_class.objects.create(
                user=user,
                company_name=company_name,
                company_reg=company_reg,
                contact_number=contact_number,
                web_address=web_address,
                physical_address=physical_address
            )

            return redirect(reverse('dashboard'))

        form = self.form_class(self.provinces_choices())
        context = {'form': form}

        return render(request, self.template_name, context)

    def provinces_choices(self):
        provinces = self.province_model_class.objects.all()
        return tuple([[p.pk, p.name] for p in provinces])

    def roles_choices(self):
        roles = Group.objects.all()
        return tuple([[r.pk, r.name] for r in roles])


class OurProducts(View):
    template_name = 'home/products.html'

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
    province_model_class = models.Province

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
        if form.is_valid():
            appliances_model = self.appliances_model_class(request.POST)
            intended_use = form.cleaned_data['intended_use']
            site_visit = bool(form.cleaned_data['site_visit'])
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            name = request.POST.getlist('name')
            need_finance = form.cleaned_data['need_finance']
            include_installation = form.cleaned_data['include_installation']

            pvt_system = models.PVTSystem.objects.create(
                need_finance = need_finance,
                include_installation=include_installation,
                intended_use = intended_use,
                possible_appliances = name,
                roof_inclination=roof_inclination,
                property_type=property_type,
                site_visit=site_visit
            )

        #pdf_name = quotation_pdf.generate_pdf(form.data)
        #return redirect('/app/view-slip/' + pdf_name)
        return redirect('/app/dashboard/')

    def appliances_choices(self):
        appliance = models.Appliance.objects.all()
        return tuple([[p.pk, p.name] for p in appliance])

    def provinces_choices(self):
        provinces = self.province_model_class.objects.all()
        return tuple([[p.pk, p.name] for p in provinces])


class OrderGeyser(View):
    template_name = 'app/geyser_order.html'
    form_class = forms.GeyserOrderForm
    address_model_class = models.PhysicalAddress
    province_model_class = models.Province

    def get(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices, request.POST)
        print form.errors
        print form.is_valid()
        if form.is_valid():
            address_model = self.address_model_class(request)
            water_collector = form.cleaned_data['water_collector']
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            required_geyser_size = form.cleaned_data['required_geyser_size']
            current_geyser_size = form.cleaned_data['current_geyser_size']
            include_installation = form.cleaned_data['include_installation']
            users_number = form.cleaned_data['users_number']
            need_finance = form.cleaned_data['need_finance']
            existing_geyser = form.cleaned_data['existing_geyser']

            contact_number = form.cleaned_data['contact_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            province_id = form.cleaned_data['province']
            province = \
                self.province_model_class.objects.filter(pk=province_id)[0]

            physical_address = self.address_model_class.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            geyser_order = models.GeyserSystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation,
                property_type=property_type,
                roof_inclination=roof_inclination,
                existing_geyser=existing_geyser,
                new_system=existing_geyser,
                water_collector=water_collector,
                current_geyser_size=current_geyser_size,
                users_number=users_number,
                required_geyser_size=required_geyser_size,
                same_as_existing=existing_geyser
            )

            client = models.Client.objects.create(
                username=username,
                lastname=last_name,
                firstname=first_name,
                contact_number=contact_number,
                physical_address=physical_address
            )

            order = models.Order.objects.create(
                client=client
            )

            system_order = models.SystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation
            )

            order_item = models.OrderItem.objects.create(
                order = order,
                system = system_order
            )

        return redirect('/app/dashboard/')


class DisplayPDF(View):

    def get(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/'
        image_data = open(pdf_dir + str(kwargs['generate']) + '.pdf',
                          "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")


class AddComponent(View):
    template_name = 'app/add_component.html'
    form_class = forms.AddComponentForm

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


class MyProducts(LoginRequiredMixin, View):
    template_name = 'app/supplier/products.html'
    user_model_class = models.SpazrUser
    products_model_class = models.Product
    userproduct_model_class = models.SpazrUserProduct
    form_class = forms.MyProductForm

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        form = self.form_class()
        user = self.user_model_class.objects.filter(user=req_user)[0]
        my_products = self.userproduct_model_class.objects.filter(user=user)
        all_products = self.products_model_class.objects.all()
        context = {'user': user, 'all_products': all_products,
                   'my_products': my_products, 'form': form}

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class()

        if form.is_valid():
            price = kwargs['price']
            product_id = kwargs['product']
            
            product = self.products_model_class.objects.filter(pk=product_id)
            user_product = self.userproduct_model_class.objects.create(
                user=request.user,
                product=product 
            )

        return render(request, self.template_name, context)


class OrderQuotes(View):
    template_name = 'app/order_quotes.html'

    def get(self, request, *args, **kwargs):
        """
        """
        
        return render(request, self.template_name) # , context)


    def get_pdf(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/'
        image_data = open(pdf_dir + str(kwargs['generate']) + '.pdf',
                          "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")
