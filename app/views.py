# Django
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q, Count
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views import View
from django.core import serializers

# Other Libraries
from registration.backends.hmac.views import ActivationView
from wsgiref.util import FileWrapper

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
    address_model_class = models.PhysicalAddress
    supplier_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices()
        form = self.form_class(p_choices)
        print form.data
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices()
        form = self.form_class(p_choices, request.POST)

        if form.is_valid():
            p_choices = self.provinces_choices()
            form = self.form_class(p_choices, request.POST)
            appliances_model = self.appliances_model_class(request.POST)

            intended_use = form.cleaned_data['intended_use']
            site_visit = form.cleaned_data['site_visit']
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            names = request.POST.getlist('name')
            need_finance = form.cleaned_data['need_finance']
            include_installation = form.cleaned_data['include_installation']

            contact_number = form.cleaned_data['contact_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']

            province_id = form.cleaned_data['province']
            province = \
                self.province_model_class.objects.filter(pk=province_id)[0]

            pvt_system = models.PVTSystem.objects.create(
                need_finance=need_finance,
                include_installation=include_installation,
                intended_use=intended_use,
                roof_inclination=roof_inclination,
                property_type=property_type,
                site_visit=site_visit
            )

            physical_address = self.address_model_class.objects.create(
                building_name=form.cleaned_data['contact_number'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            client = models.Client.objects.create(
                username=username,
                lastname=last_name,
                firstname=first_name,
                contact_number=contact_number,
                physical_address=physical_address
            )

            supplier = self.supplier_model_class.objects.filter(user=request.user)[0]
            order = models.Order.objects.create(
                client=client,
                supplier=supplier
            )

            system_order = models.SystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation
            )

            order_item = models.OrderItem.objects.create(
                order = order,
                system = system_order
            )

            for name in names:
                id_name = models.Appliance.objects.filter(name=name)[0]
                pvt_system.possible_appliances.add(id_name)

        # pdf_name = quotation_pdf.generate_pdf(form.data)
        # return redirect('/app/view-slip/' + pdf_name)
        return redirect('/app/order-quotes/' +
                        str(pvt_system.systemorder_ptr_id))

    def appliances_choices(self):
        appliance = models.Appliance.objects.all()
        return tuple([[p.pk, p.name] for p in appliance])

    def provinces_choices(self):
        provinces = self.province_model_class.objects.all()
        return tuple([[p.pk, p.name] for p in provinces])


class OrderGeyser(LoginRequiredMixin, View):
    template_name = 'app/geyser_order.html'
    form_class = forms.GeyserOrderForm
    address_model_class = models.PhysicalAddress
    province_model_class = models.Province
    supplier_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices, request.POST)
        print form.errors
        if form.is_valid():
            address_model = self.address_model_class(request)

            water_collector = form.cleaned_data['water_collector']
            property_type = form.cleaned_data['property_type']
            roof_inclination = form.cleaned_data['roof_inclination']
            required_geyser_size = form.cleaned_data['required_geyser_size']
            include_installation = form.cleaned_data['include_installation']
            users_number = form.cleaned_data['users_number']
            need_finance = form.cleaned_data['need_finance']

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
            
            system_order = models.SystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation
            )

            geyser_order = models.GeyserSystemOrder.objects.create(
                property_type=property_type,
                roof_inclination=roof_inclination,
                water_collector=water_collector,
                users_number=users_number,
                required_geyser_size=required_geyser_size,
                order_number=system_order.order_number
            )
            
            client = models.Client.objects.create(
                username=username,
                lastname=last_name,
                firstname=first_name,
                contact_number=contact_number,
                physical_address=physical_address
            )

            supplier = self.supplier_model_class.objects.filter(user=request.user)[0]
            order = models.Order.objects.create(
                client=client,
                supplier=supplier,
                order_number= models.SystemOrder.objects.filter(order_number=system_order.order_number)[0]
            )
            pdf_name = quotation_pdf.generate_pdf(client, order, physical_address,
                                                  system_order, supplier)
        return redirect('/app/order-quotes/' +
                        str(system_order.order_number) )


class DisplayPDF(View):
    def get(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/'
        image_data = open(pdf_dir + str(kwargs['generate']) + '.pdf', "r")

        response = HttpResponse(FileWrapper(image_data), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + str(
            kwargs['generate'])+'.pdf'
        image_data.close()
        return response


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
    # edit_form_class = forms.EditProductForm
    edit_panel_form_class = forms.EditPanelForm
    panel_size_class = models.PanelSize

    new_form_class = forms.NewProductForm

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        edit_panel_form = self.edit_panel_form_class
        new_form = self.new_form_class()
        averages = []

        all_prods = self.products_model_class.objects.annotate(
            count=Count('spazruserproduct')
        )
        user = self.user_model_class.objects.filter(user=req_user)[0]
        my_prods = self.products_model_class.objects\
            .filter(spazruserproduct__user=user).annotate(
                count=Count('spazruserproduct')
        )

        context = {'user': user, 'averages': averages, 'my_products': my_prods,
                   'all_products': all_prods, 'edit_form': edit_panel_form,
                   'new_form': new_form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        edit_form = self.edit_form_class(request.POST)
        new_form = self.new_form_class(request.POST)

        if edit_form.is_valid():
            prod_id = edit_form.cleaned_data['edit_prod_id']
            prod = self.products_model_class.objects.filter(pk=prod_id)[0]
            user = self.user_model_class.objects.filter(user=request.user)[0]
            price = edit_form.cleaned_data['edit_price']
            user_prod = self.userproduct_model_class.objects.filter(
                Q(user=user),
                Q(product=prod)
            )
            if len(user_prod):
                my_prod = user_prod[0]
                my_prod.price = price
                my_prod.save()
            else:
                self.userproduct_model_class.objects.create(
                    user=user,
                    product=prod,
                    price=price
                )
        elif new_form.is_valid():
            name = new_form.cleaned_data['new_name']
            price = new_form.cleaned_data['new_price']
            product = self.products_model_class.objects.create(name=name)
            user = self.user_model_class.objects.filter(user=request.user)[0]
            user_product = self.userproduct_model_class.objects.create(
                user=user,
                product=product,
                price=price
            )

        return redirect(reverse('my-products'))


class OrderQuotes(View):
    template_name = 'app/order_quotes.html'

    def get(self, request, *args, **kwargs):
        """
        """
        #systemorder_ptr_id
        user_id = kwargs['user_id']
        data = models.GeyserSystemOrder.objects.filter(systemorder_ptr_id =
                                                   user_id)
        products = models.Product.objects.all()
        context = {'data': data, 'products':products}
        return render(request, self.template_name, context) # , context)

    def post(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/'
        image_data = open(pdf_dir + str(kwargs['generate']) + '.pdf',
                          "rb")
        response = HttpResponse(FileWrapper(image_data),
                                content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=quotation.pdf'
        return response


class MyQuotes(LoginRequiredMixin, View):
    template_name = 'app/supplier/quotes.html'
    user_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        user = self.user_model_class.objects.filter(user=req_user)[0]
        
        orders = models.Order.objects.values()
        print 'ORDERS: ', [ i for i in orders]
        for order in orders:
            client_names = models.Client.objects.filter(id=order['client_id'])[0]
            orders['name'] = client_names.username
            print orders['name']
        #print orders
        context = {'user': user, 'quotes': quotes}

        return render(request, self.template_name, context)

