from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.db import transaction
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum

from apps.cashier.forms import ProductForm, BuyForm, DetailBuyForm, Product_Stock_Form
from apps.entity.models import Pet, Client, Provider
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct

from apps.entity.mixins import Perms_Check

class BuyViews(Perms_Check, TemplateView):
    template_name = 'buy/buys.html'
    permission_required = 'cashier.view_detail_bs'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Buy_Sale.objects.filter(type_bs='Compra'):
                    data.append(i.toJSON())
            elif action == 'detail':
                data = []
                for i in Detail_BS.objects.filter(buy_sale_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'delete':
                perms = ('cashier.delete_buy_sale',)
                if request.user.has_perms(perms):

                    with transaction.atomic():

                        for det in Detail_BS.objects.filter(buy_sale=request.POST['id']):
                            prod = ChildProduct.objects.filter(pk=det.product.id).first()
                            prod.stock -= det.stock
                            if prod.stock < 0:
                                prod.stock = 0
                            prod.save()
                            
                            cont = ChildProduct.objects.filter(product__name=prod.product.name).aggregate(Sum('stock'))
                            prod_parent = Product.objects.filter(pk=prod.product.id).first()
                            prod_parent.stock = cont['stock__sum'] 
                            prod_parent.save()

                        buy = Buy_Sale.objects.get(pk=request.POST['id'])            
                        buy.delete() 
                else:
                    data['error'] = 'No tiene permisos para eliminar un producto'
            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Compras'
        context['sub_titulo'] = 'Listado de Compras'
        context['navegacion'] = 'Compras'
        context['list_url'] = reverse_lazy('cashier:products')
        return context

class Create_Buy(Perms_Check, SuccessMessageMixin, CreateView):
    template_name = 'buy/form_buy.html'
    permission_required = 'cashier.view_detail_bs'
    model = Buy_Sale
    form_class = BuyForm
    success_massage = 'La compra ha sido registrada correctamente'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:15]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 
                
                    buy = Buy_Sale()
                    buy.provider_id = vents['provider']
                    buy.type_bs = vents['type_bs']
                    buy.sub_total = float(vents['subtotal'])
                    buy.iva = float(vents['iva'])
                    buy.total = float(vents['total'])
                    buy.save()

                    for i in vents['products']:
                        filter_prod = ChildProduct.objects.filter(product__name=i['name']).filter(date_conquered = i['date_conquered']).first()
                        if filter_prod:

                            prod = ChildProduct.objects.filter(product__name=i['name']).filter(date_conquered = i['date_conquered']).first()
                            prod.product_id = i['id']
                            prod.stock += int(i['stock'])
                            prod.price_buy = float(i['price_buy'])
                            prod.price_sale = float(i['price_sale'])
                            prod.date_conquered = i['date_conquered']
                            prod.profit = float(i['profit'])
                            prod.save()

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = prod.id
                            det.stock = int(i['stock'])
                            det.total = float(i['total'])
                            det.profit = float(det.stock * i['profit'])
                            det.save() 

                        else:
                            prod = ChildProduct()
                            prod.product_id = i['id']
                            prod.stock = int(i['stock'])
                            prod.price_buy = float(i['price_buy'])
                            prod.price_sale = float(i['price_sale'])
                            prod.date_conquered = i['date_conquered']
                            prod.profit = float(i['profit'])
                            prod.save()

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = prod.id
                            det.stock = int(i['stock'])
                            det.total = float(i['total'])
                            det.profit = float(det.stock * i['profit'])
                            det.save() 

            else:
                data['error'] = 'Ha ocurrido un error'
                
        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Registar Compra'
        context['sub_titulo'] = 'Registro de Compra'
        context['navegacion'] = 'Registrar Compra'
        context['navegacion2'] = 'Compras'
        context['list_url'] = reverse_lazy('cashier:buys')
        context['action'] = 'add'
        context['det'] = []
        return context


class Edit_Buy(Perms_Check, SuccessMessageMixin, UpdateView):

    template_name = 'buy/form_buy.html'
    permission_required = 'cashier.change_buy_sale'
    model = Buy_Sale
    form_class = BuyForm
    success_massage = 'La compra ha sido modificada correctamente'


    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:15]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'edit':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 
                
                    buy = self.get_object()
                    buy.provider_id = vents['provider']
                    buy.type_bs = vents['type_bs']
                    buy.sub_total = float(vents['subtotal'])
                    buy.iva = float(vents['iva'])
                    buy.total = float(vents['total'])
                    buy.save()

                    for i in Detail_BS.objects.filter(buy_sale=self.get_object()):
                        ChildProduct.objects.filter(pk=i.product_id).delete()
                    Detail_BS.objects.filter(buy_sale=self.get_object()).delete()

                    for i in vents['products']:
                        filter_prod = ChildProduct.objects.filter(product__name=i['name']).filter(date_conquered = i['date_conquered']).first()
                        if filter_prod:

                            prod = ChildProduct.objects.filter(product__name=i['name']).filter(date_conquered = i['date_conquered']).first()
                            prod.product_id = i['id']
                            prod.stock += int(i['stock'])
                            prod.price_buy = float(i['price_buy'])
                            prod.price_sale = float(i['price_sale'])
                            prod.date_conquered = i['date_conquered']
                            prod.profit = float(i['profit'])
                            prod.save()

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = prod.id
                            det.stock = int(i['stock'])
                            det.total = float(i['total'])
                            det.profit = float(det.stock * i['profit'])
                            det.save() 
                        else:
                            prod = ChildProduct()
                            prod.product_id = i['id']
                            prod.stock = int(i['stock'])
                            prod.price_buy = float(i['price_buy'])
                            prod.price_sale = float(i['price_sale'])
                            prod.date_conquered = i['date_conquered']
                            prod.profit = float(i['profit'])
                            prod.save()

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = prod.id
                            det.stock = int(i['stock'])
                            det.total = float(i['total'])
                            det.profit = float(det.stock * i['profit'])
                            det.save() 

            else:
                data['error'] = 'Ha ocurrido un error'
                
        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)
    
    def get_detail(self):
        data = []
        try:
            for i in Detail_BS.objects.filter(buy_sale_id=self.get_object().id):
                item = i.product.toJSON()
                item['stock'] = i.stock
                item['name'] = i.product.product.name
                item['id'] = i.product.product.id
                item['id_child'] = i.product.id


                data.append(item)

        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Editar Compra'
        context['sub_titulo'] = 'Editar de Compra'
        context['navegacion'] = 'Editar Compra'
        context['navegacion2'] = 'Compras'
        context['list_url'] = reverse_lazy('cashier:buys')
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
        return context

