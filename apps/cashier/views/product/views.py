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

from apps.cashier.forms import ProductForm
from apps.cashier.models import Product

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
            
            elif action == 'edit':
                perms = ('cashier.change_product',)
                if request.user.has_perms(perms):
                    pro = Product.objects.get(pk=request.POST['id'])
                    pro.name = request.POST.get('name')
                    pro.stock = request.POST.get('stock')
                    pro.price_buy = request.POST.get('price_buy')
                    pro.price_sale = request.POST.get('price_sale')
                    pro.date_conquered = request.POST.get('date_conquered')
                    pro.profit = request.POST.get('profit')
                    pro.num_sales = request.POST.get('num_sales')
                    pro.type_stock = request.POST.get('type_stock')
                    pro.quantity = request.POST.get('quantity')
                    pro.status = 'status' in request.POST
                    pro.save()
                else:
                    data['error'] = 'No tiene permisos para editar una mascota'      

            elif action == 'delete':
                perms = ('cashier.delete_product',)
                if request.user.has_perms(perms):
                    pro = Product.objects.get(pk=request.POST['id'])            
                    pro.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar una mascota'
            
            elif action == 'btn-estado':
                perms = ('cashier.change_product',)
                if request.user.has_perms(perms):
                    pro = Product.objects.get(pk=request.POST['id'])
                    if pro.status:
                        pro.status = False
                        pro.save()
                    else:
                        pro.status = True
                        pro.save()
                else:
                    data['error'] = 'No tiene permisos para editar una mascota'  

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