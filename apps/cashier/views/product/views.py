from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from datetime import datetime
import json

from apps.cashier.forms import ProductForm
from apps.cashier.models import Product, ChildProduct

from apps.entity.mixins import Perms_Check

# CRUD PETS URL
class ProductViews(Perms_Check, TemplateView):
    template_name = 'product/products.html'
    permission_required = 'cashier.view_product'

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
                for i in Product.objects.filter(status = True ):
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('cashier.add_product',)
                if request.user.has_perms(perms):
                    pro = Product()
                    pro.name = request.POST.get('name')
                    pro.stock = request.POST.get('stock')
                    pro.type_stock = request.POST.get('type_stock')
                    pro.quantity = request.POST.get('quantity')
                    pro.save()
                else: data['error'] = 'No tienes permisos para registrar un producto'
            
            elif action == 'edit':
                perms = ('cashier.change_product',)
                if request.user.has_perms(perms):
                    pro = Product.objects.get(pk=request.POST['id'])
                    pro.name = request.POST.get('name')
                    pro.stock = request.POST.get('stock')
                    pro.type_stock = request.POST.get('type_stock')
                    pro.quantity = request.POST.get('quantity')
                    pro.save()
                else:
                    data['error'] = 'No tiene permisos para editar un producto'      

            elif action == 'delete':
                perms = ('cashier.delete_product',)
                if request.user.has_perms(perms):
                    pro = Product.objects.get(pk=request.POST['id'])            
                    pro.delete()
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
        context['titulo'] = 'SISVET | Listado de Productos'
        context['sub_titulo'] = 'Listado de Productos'
        context['navegacion'] = 'Productos'
        context['form'] = ProductForm()
        context['list_url'] = reverse_lazy('cashier:products')
        return context

def detail_product(request, id):
    template_name = 'product/detail_pro.html'
    context = {}

    if id:
        prod = Product.objects.filter(pk = id).first()
        stock = ChildProduct.objects.filter(product = id).filter(stock__gt=0)

        context = {
            'prod': prod,
            'stock': stock
        }

    else:
        context = {
            'prod': 'No hay datos',
            'stock': 'No hay datos'
        }

    return render(request, template_name, context)
