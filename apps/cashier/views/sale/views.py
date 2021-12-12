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
from datetime import date
from django.db.models import Sum

from apps.cashier.forms import ProductForm, BuyForm, DetailBuyForm, Product_Stock_Form, DollarForm
from apps.entity.models import Pet, Client, Provider
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct
from apps.usersys.models import DollarStatus

from apps.entity.mixins import Perms_Check

class SaleViews(Perms_Check, TemplateView):
    template_name = 'sale/sales.html'
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
                for i in Buy_Sale.objects.filter(type_bs='Venta'):
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
                            prod.stock += det.stock
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
        context['titulo'] = 'SISVET | Listado de Ventas'
        context['sub_titulo'] = 'Listado de Ventas'
        context['navegacion'] = 'Ventas'
        context['list_url'] = reverse_lazy('cashier:products')
        return context


class Create_Sale(Perms_Check, SuccessMessageMixin, CreateView):
    template_name = 'sale/form_sale.html'
    permission_required = 'cashier.change_detail_bs'
    model = Buy_Sale
    form_class = BuyForm
    success_massage = 'La venta ha sido registrada correctamente'

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
                ids_exclude = json.loads(request.POST['ids'])
                prods = ChildProduct.objects.filter(product__name__icontains=request.POST['term']).filter(stock__gt=0).order_by('date_conquered')
                for i in prods.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = '{} {}'.format(i.product.name, i.date_conquered.strftime('%d-%m-%Y'))
                    item['name'] = i.product.name
                    item['exist_stock'] = i.stock
                    item['date_conquered_2'] = i.date_conquered.strftime('%d-%m-%Y')
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 

                    price_dollar = DollarStatus.objects.get(pk=1)
                    price_dollar.price_dollar = vents['price_dollar']
                    price_dollar.save()
                
                    buy = Buy_Sale()
                    buy.client_id = vents['client']
                    buy.type_bs = vents['type_bs']
                    buy.sub_total = float(vents['subtotal'])
                    buy.iva = float(vents['iva'])
                    buy.total = float(vents['total'])
                    buy.total_bs = float(vents['total_bs'])
                    buy.price_dollar = float(vents['price_dollar'])
                    buy.save()

                    for i in vents['products']:

                            prod_child = ChildProduct.objects.get(pk = i['id'])
                            prod_child.stock = prod_child.stock - int(i['stock']) 
                            prod_child.save()

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = i['id']
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

    def get_price_dollar(self):
        get_dollar = DollarStatus.objects.get(pk=1)
        price = get_dollar.price_dollar
        return float(price)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Registar Venta'
        context['sub_titulo'] = 'Registro de Venta'
        context['navegacion'] = 'Registrar Venta'
        context['navegacion2'] = 'Ventas'
        context['list_url'] = reverse_lazy('cashier:sales')
        context['action'] = 'add'
        context['form_dollar'] = DollarForm()
        context['get_dollar'] = self.get_price_dollar()
        context['det'] = []
        return context

class Edit_Sale(Perms_Check, SuccessMessageMixin, UpdateView):
    template_name = 'sale/form_sale_edit.html'
    permission_required = 'cashier.change_buy_sale'
    model = Buy_Sale
    form_class = BuyForm
    success_massage = 'La venta ha sido modificada correctamente'


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
                ids_exclude = json.loads(request.POST['ids'])
                prods = ChildProduct.objects.filter(product__name__icontains=request.POST['term']).filter(stock__gt=0).order_by('date_conquered')
                for i in prods.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = '{}: {}'.format(i.product.name, i.date_conquered)
                    item['name'] = i.product.name
                    item['exist_stock'] = i.stock
                    item['date_conquered_2'] = i.date_conquered.strftime('%d-%m-%Y')
                    data.append(item)

            elif action == 'edit':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 
                
                    buy = self.get_object()
                    buy.client_id = vents['client']
                    buy.type_bs = vents['type_bs']
                    buy.sub_total = float(vents['subtotal'])
                    buy.iva = float(vents['iva'])
                    buy.total = float(vents['total'])
                    buy.total_bs = float(vents['total_bs'])
                    buy.price_dollar = float(vents['price_dollar'])
                    buy.save()

                    for i in Detail_BS.objects.filter(buy_sale=self.get_object()):
                        for e in ChildProduct.objects.filter(pk=i.product_id):
                            e.stock = e.stock + int(i.stock)
                            e.save()
                    Detail_BS.objects.filter(buy_sale=self.get_object()).delete()

                    for i in vents['products']:

                            prod_child = ChildProduct.objects.get(pk = i['id'])
                            prod_child.stock = prod_child.stock - int(i['stock']) 
                            prod_child.save()  

                            det = Detail_BS()
                            det.buy_sale_id = buy.id
                            det.product_id = i['id']
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
                item['exist_stock'] = i.product.stock + i.stock
                data.append(item)

        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Editar Venta'
        context['sub_titulo'] = 'Editar de Venta'
        context['navegacion'] = 'Editar Venta'
        context['navegacion2'] = 'Ventas'
        context['list_url'] = reverse_lazy('cashier:sales')
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
        return context

