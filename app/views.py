import json

# Django
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.core import serializers
from django.db.models import Q, Count, Min
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views import View
from django.views.generic import TemplateView

# Other Libraries
from registration.backends.hmac.views import ActivationView
from wsgiref.util import FileWrapper

# Local Django
from app import forms
from app import models
from app.utils import quotation_pdf
from app.utils.send_pdf import TransactionVerification


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
    cart_model_class = models.Cart

    def get(self, request, *args, **kwargs):
        """
        """
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        session_user = Session.objects.get(pk=session_key)

        prods = models.GeneralProduct.objects.exclude(
            cart__session_user=session_user
        ).values(
            'brand__product'
        ).annotate(
            pcount=Count('brand__product'),
        )

        dims = map(
            lambda prod: MyProducts()._prepare_dimensions(
                models.GeneralProduct.objects.exclude(
                    cart__session_user=session_user).filter(
                        brand__product=prod['brand__product'],
                ).values(
                    'id',
                    'brand__name',
                    'dimensions__name',
                    'dimensions__value'
                )
            ),
            prods
        )

        all_prods = map(
            lambda prod: dict(prod[0], dimensions=prod[1]),
            zip(prods, dims)
        )

        all_prods_json = json.dumps(all_prods)

        my_prods = self.cart_model_class.objects.filter(session_user=session_user).values(
            'product__brand__product__name',
            'product__brand__name__name',
            'product__dimensions',
            'quantity',
        )

        for prod in my_prods:
            id = prod['product__dimensions']
            dimension = models.Dimension.objects.get(id=id)
            # value = dimension.name.name + ": " + dimension.value
            prod['product__dimensions'] = [
                {'name': dimension.name.name, 'value': dimension.value}
            ]
        # .product__dimensions
        print my_prods[0]['product__dimensions'][0]['value']
        context = {'my_products': my_prods,
                   'all_products': all_prods, 'json_all_prods': all_prods_json}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        products_model_class = models.Product
        user_model_class = Session

        user = user_model_class.objects.get(pk=request.session.session_key)

        product = products_model_class.objects.filter(
            name=request.POST.get('product')
        )[0]

        str_dimensions = request.POST.getlist('dimensions')
        product_brandname = models.ProductBrandName.objects.filter(
            name=request.POST.get('brand_name')
        )
        product_brand = models.ProductBrand.objects.filter(
            name=product_brandname,
            product=product
        )
        dimensions = map(lambda dim: dim.split(','), str_dimensions)
        dimensions = map(lambda dim: models.Dimension.objects.filter(
            name=models.DimensionName.objects.filter(
                name=dim[0].capitalize()
            ),
            value=dim[1],
            product=product
        )[0],
            dimensions
        )
        list_dimensions = []
        for dim in dimensions:
            list_dimensions.append(dim)

        general_product = models.GeneralProduct.objects.filter(
            brand=product_brand,
            dimensions__in=list_dimensions
        )[0]

        # Check if product already exists
        cart = self.cart_model_class.objects.filter(
            session_user=user,
            product=general_product,
        )

        quantity = request.POST.get('quantity')

        if len(cart):
            update = cart[0]
            update.quantity = quantity
            update.save()
        else:
            self.cart_model_class.objects.update_or_create(
                session_user=user,
                product=general_product,
                quantity=quantity,
            )

        return redirect(reverse('user-cart'))


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

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        """
        p_choices = self.provinces_choices()
        appliances_model = self.appliances_model_class(request.POST)
        form = self.form_class(p_choices, request.POST)

        if form.is_valid():
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
            province = self.province_model_class.objects.filter(pk=province_id)[
                0]

            client = models.Client.objects.filter(username=username)
            physical_address = ''

            if len(client) == 0:
                physical_address = self.address_model_class.objects.create(
                    building_name=form.cleaned_data['building_name'],
                    street_name=form.cleaned_data['street_name'],
                    suburb=form.cleaned_data['suburb'],
                    province=province,
                    city=form.cleaned_data['city'],
                    zip_code=form.cleaned_data['zip_code']
                )

                models.Client.objects.create(
                    username=username,
                    lastname=last_name,
                    firstname=first_name,
                    contact_number=contact_number,
                    physical_address=physical_address
                )

                client = models.Client.objects.filter(username=username)
            else:
                self.address_model_class.objects.filter(
                    address_id=client[0].physical_address_id).update(
                        building_name=form.cleaned_data['building_name'],
                        street_name=form.cleaned_data['street_name'],
                        suburb=form.cleaned_data['suburb'],
                        province=province,
                        city=form.cleaned_data['city'],
                        zip_code=form.cleaned_data['zip_code']
                )
                physical_address = self.address_model_class.objects.filter(
                    address_id=client[0].physical_address_id)[0]

                models.Client.objects.filter(username=username).update(
                    username=username,
                    lastname=last_name,
                    firstname=first_name,
                    contact_number=contact_number,
                    physical_address=physical_address
                )
                client = models.Client.objects.filter(username=username)

            system_order = models.SystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation
            )

            order_number = models.SystemOrder.objects.filter(
                order_number=system_order.order_number)[0]

            pvt_system = models.PVTSystem.objects.create(
                intended_use=intended_use,
                roof_inclination=roof_inclination,
                property_type=property_type,
                site_visit=site_visit,
                order_number=order_number
            )

            # .filter(user=request.user)[0]
            suppliers = self.supplier_model_class.objects.all()
            for supplier in suppliers:
                order = models.Order.objects.create(
                    client=client[0],
                    supplier=supplier,
                    order_number=order_number
                )
                pdf_name = quotation_pdf.generate_pdf(client[0],
                                                      system_order)

        # pdf_name = quotation_pdf.generate_pdf(form.data)
        # return redirect('/app/view-slip/' + pdf_name)
        return redirect('/app/order-quotes/' +
                        str(system_order.order_number))

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
    supplier_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        p_choices = OrderPVTSystem().provinces_choices
        form = self.form_class(p_choices, request.POST)

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
                self.province_model_class.objects.get(pk=province_id)

            client = models.Client.objects.filter(username=username)
            physical_address = ''

            if len(client) == 0:
                physical_address = self.address_model_class.objects.create(
                    building_name=form.cleaned_data['building_name'],
                    street_name=form.cleaned_data['street_name'],
                    suburb=form.cleaned_data['suburb'],
                    province=province,
                    city=form.cleaned_data['city'],
                    zip_code=form.cleaned_data['zip_code']
                )

                models.Client.objects.create(
                    username=username,
                    lastname=last_name,
                    firstname=first_name,
                    contact_number=contact_number,
                    physical_address=physical_address
                )

                client = models.Client.objects.filter(username=username)
            else:
                self.address_model_class.objects.filter(
                    address_id=client[0].physical_address_id).update(
                        building_name=form.cleaned_data['building_name'],
                        street_name=form.cleaned_data['street_name'],
                        suburb=form.cleaned_data['suburb'],
                        province=province,
                        city=form.cleaned_data['city'],
                        zip_code=form.cleaned_data['zip_code']
                )
                physical_address = self.address_model_class.objects.get(
                    address_id=client[0].physical_address_id)

                models.Client.objects.filter(username=username).update(
                    username=username,
                    lastname=last_name,
                    firstname=first_name,
                    contact_number=contact_number,
                    physical_address=physical_address
                )
                client = models.Client.objects.filter(username=username)[0]

            system_order = models.SystemOrder.objects.create(
                need_finance=need_finance,
                include_installation=include_installation
            )

            order_number = models.SystemOrder.objects.filter(
                order_number=system_order.order_number)[0]

            geyser_order = models.GeyserSystemOrder.objects.create(
                property_type=property_type,
                roof_inclination=roof_inclination,
                water_collector=water_collector,
                users_number=users_number,
                required_geyser_size=required_geyser_size,
                order_number=order_number
            )

            suppliers = self.supplier_model_class.objects.all()
            for supplier in suppliers:
                order = models.Order.objects.create(
                    client=client[0],
                    supplier=supplier,
                    order_number=order_number
                )
                pdf_name, status = quotation_pdf.generate_pdf(client[0],
                                                              system_order)

        return redirect('/app/order-quotes/' +
                        str(system_order.order_number) + '/' + str(status))


class DisplayPDF(View):
    def get(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/' + str(kwargs['generate']) + '_' + \
                  str(kwargs['pdf']) + '.pdf'
        fw = open(pdf_dir, "r")
        response = HttpResponse(FileWrapper(
            fw), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + str(
            kwargs['generate']) + '_' + str(kwargs['pdf']) + '.pdf'
        fw.close()
        return response


class AddComponent(View):
    template_name = 'app/add_component.html'
    form_class = forms.AddComponentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)


class MyProducts(LoginRequiredMixin, View):
    template_name = 'app/supplier/products.html'
    user_model_class = models.SpazrUser
    products_model_class = models.Product
    userproduct_model_class = models.SellingProduct
    edit_panel_form_class = forms.EditPanelForm
    new_form_class = forms.NewProductForm

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        edit_panel_form = self.edit_panel_form_class
        new_form = self.new_form_class()
        averages = []
        user = self.user_model_class.objects.filter(user=req_user)[0]

        # All products with count of different brands for each product
        prods = models.GeneralProduct.objects.exclude(
            sellingproduct__user=user
        ).values(
            'brand__product'
        ).annotate(
            pcount=Count('brand__product'),
        )

        dims = map(
            lambda prod: self._prepare_dimensions(
                models.GeneralProduct.objects.exclude(
                    sellingproduct__user=user).filter(
                        brand__product=prod['brand__product'],
                ).values(
                    'id',
                    'brand__name',
                    'dimensions__name',
                    'dimensions__value'
                )
            ),
            prods
        )

        all_prods = map(
            lambda prod: dict(prod[0], dimensions=prod[1]),
            zip(prods, dims)
        )

        all_prods_json = json.dumps(all_prods)

        my_prods = self.userproduct_model_class.objects.filter(user=user).values(
            'product__brand__product__name',
            'product__brand__name__name',
            'product__dimensions',
            'price',
        )

        for prod in my_prods:
            id = prod['product__dimensions']
            dimension = models.Dimension.objects.get(id=id)
            prod['product__dimensions'] = [
                {'name': dimension.name.name, 'value': dimension.value}
            ]

        context = {'user': user, 'averages': averages, 'my_products': my_prods,
                   'all_products': all_prods, 'json_all_prods': all_prods_json,
                   'edit_form': edit_panel_form, 'new_form': new_form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print request.POST
        product = self.products_model_class.objects.filter(
            name=request.POST.get('product')
        )[0]
        user = self.user_model_class.objects.filter(user=request.user)[0]
        str_dimensions = request.POST.getlist('dimensions')
        product_brandname = models.ProductBrandName.objects.filter(
            name=request.POST.get('brand_name')
        )
        product_brand = models.ProductBrand.objects.get(
            name=product_brandname,
            product=product
        )
        dimensions = map(lambda dim: dim.split(','), str_dimensions)
        dimensions = map(lambda dim: models.Dimension.objects.filter(
            name=models.DimensionName.objects.filter(
                name=dim[0].capitalize()
            ),
            value=dim[1],
            product=product
        )[0],
            dimensions
        )

        list_dimensions = []
        for dim in dimensions:
            list_dimensions.append(dim)



        general_product = models.GeneralProduct.objects.filter(
            brand=product_brand,
            dimensions__in=list_dimensions
        )[0]

        print general_product.dimensions

        # Check if product already exists
        selling = self.userproduct_model_class.objects.filter(
            user=user,
            product=general_product,
        )

        price = float(request.POST.get('price'))

        if len(selling):
            update = selling[0]
            update.price = price
            update.save()
        else:
            self.userproduct_model_class.objects.update_or_create(
                user=user,
                product=general_product,
                price=float(request.POST.get('price')),
            )

        return redirect(reverse('my-products'))

    def _prepare_dimensions(self, dimensions):
        """
        Compile the list of dimensions for the product in the
        formart needed by front-end.

        Args:
            dimensions (Queryset): list of all dimensions for the
                product.

        Returns:
            Formated output of the dimensions.

        """
        result = {'brand': []}
        ids = []

        for item in dimensions:
            key = item['dimensions__name'].lower().replace(' ', '_')
            value = item['dimensions__value']
            if key in result:
                result[key].append(value)
            else:
                result[key] = [value]
            if item['id'] not in ids:
                result['brand'].append(item['brand__name'])
                ids.append(item['id'])

        return result


class OrderQuotes(View):
    template_name = 'app/order_quotes.html'

    def get(self, request, *args, **kwargs):
        """
        """
        # systemorder_ptr_id
        order_number = kwargs['order_number']
        order_status = kwargs['status']
        if order_status == 1:
            order_status = True
        else:
            order_status = False
        data = models.GeyserSystemOrder.objects.filter(
            order_number=order_number)
        products = models.Product.objects.all()
        context = {'data': data, 'products': products, 'user_id': order_number,
                   'order_status': order_status}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pdf_dir = 'app/static/app/slips/' + str(kwargs['generate']) + '.pdf'
        fw = open(pdf_dir, "rb")
        response = HttpResponse(FileWrapper(
            fw), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=quotation.pdf'
        return response


class MyQuotes(LoginRequiredMixin, View):
    template_name = 'app/supplier/quotes.html'
    user_model_class = models.SpazrUser

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user
        spazar_user = self.user_model_class.objects.filter(user=req_user)[0]

        orders = models.Order.objects.filter(
            supplier_id=spazar_user.user_id)

        clients = []
        for order in orders:
            clients.append(models.Client.objects.filter(
                client_id=order.client_id)[0])

        data = zip(orders, clients)

        context = {'user': spazar_user, 'data': data}

        return render(request, self.template_name, context)


class UserAccount(LoginRequiredMixin, View):
    template_name = 'app/supplier/account.html'
    form_class = forms.UserAccountForm
    address_model_class = models.PhysicalAddress
    user_model_class = models.SpazrUser
    province_model_class = models.Province

    def get(self, request, *args, **kwargs):
        """
        """
        req_user = request.user

        spazar_user = models.SpazrUser.objects.filter(user=req_user)[0]

        address = models.PhysicalAddress.objects.filter(
            address_id=spazar_user.physical_address_id)[0]

        p_choices = self.provinces_choices
        form = self.form_class(p_choices)

        context = {'form': form, 'user': spazar_user, 'address': address}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        p_choices = self.provinces_choices
        form = self.form_class(p_choices, request.POST)

        if form.is_valid():
            address_model = self.address_model_class(request.POST)
            user = request.user

            email = form.cleaned_data['email']
            company_name = form.cleaned_data['company_name']
            web_address = form.cleaned_data['web_address']
            province_id = form.cleaned_data['province']
            province = self.province_model_class.objects.filter(pk=province_id)[
                0]

            auth_user = User.objects.get(
                username=user).id

            this_user = models.SpazrUser.objects.filter(
                user_id=auth_user)[0]

            self.address_model_class.objects.filter(
                id=this_user.physical_address_id).update(
                building_name=form.cleaned_data['building_name'],
                street_name=form.cleaned_data['street_name'],
                suburb=form.cleaned_data['suburb'],
                province=province,
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code']
            )

            User.objects.filter(username=user).update(
                email=email
            )

            self.user_model_class.objects.filter(id=this_user.user_id).update(
                company_name=company_name,
                contact_number=form.cleaned_data['contact_number'],
                web_address=web_address
            )

        form = self.form_class(self.provinces_choices())

        return redirect(reverse('my-account'))

    def provinces_choices(self):
        provinces = self.province_model_class.objects.all()
        return tuple([[p.pk, p.name] for p in provinces])


class SendEmail(View):
    def get(self, request, *args, **kwargs):
        order = kwargs['uuid']
        quote = kwargs['order']
        email = models.Client.objects.get(
            client_id=models.Order.objects.filter(order_number_id=order)[0].client_id).username
        data = {'email': email, 'domain': '127.0.0.1:8000'}
        tv = TransactionVerification(data, order, quote)
        tv.send_verification_mail()
        status = str(1)
        return redirect('/app/order-quotes/' + order + '/' + status)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class MyProductsData(JSONResponseMixin, TemplateView): 
    def render_to_response(self, content, **response_kwargs):
        req_user = content['view'].request.user
        user = models.SpazrUser.objects.get(user=req_user)
        my_prods = models.SellingProduct.objects.filter(user=user).values(
            'product__brand__product__name',
            'product__brand__name__name',
            'product__dimensions',
            'price',
        )

        return self.render_to_json_response(
            list(my_prods),
            safe=False,
            **response_kwargs
        )


class AllProductsData(JSONResponseMixin, TemplateView): 
    def render_to_response(self, content, **response_kwargs):
        req_user = content['view'].request.user
        user = models.SpazrUser.objects.get(user=req_user)

        # All products with count of different brands for each product
        prods = models.GeneralProduct.objects.exclude(
            sellingproduct__user=user
        ).values(
            'brand__product'
        ).annotate(
            pcount=Count('brand__product'),
        )

        dims = map(
            lambda prod: MyProducts()._prepare_dimensions(
                models.GeneralProduct.objects.exclude(
                    sellingproduct__user=user).filter(
                        brand__product=prod['brand__product'],
                ).values(
                    'id',
                    'brand__name',
                    'dimensions__name',
                    'dimensions__value'
                )
            ),
            prods
        )

        all_prods = map(
            lambda prod: dict(prod[0], dimensions=prod[1]),
            zip(prods, dims)
        )

        return self.render_to_json_response(
            all_prods,
            safe=False,
            **response_kwargs
        )
