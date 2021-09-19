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

from apps.cashier.forms import ProductForm, BuyForm, DetailBuyForm
from apps.entity.models import Pet, Client, Provider
from apps.cashier.models import Product, Buy_Sale, Detail_BS

from apps.entity.mixins import Perms_Check

# CRUD PETS URL
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
                for i in Buy_Sale.objects.all():
                    data.append(i.toJSON())

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
        context['form_pro'] = ProductForm()
        context['form_buy'] = BuyForm()
        context['form_buy_detail'] = DetailBuyForm()
        context['list_url'] = reverse_lazy('cashier:products')
        return context

class Create_Buy(Perms_Check, TemplateView):
    template_name = 'buy/form_buy.html'
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
                for i in Buy_Sale.objects.all():
                    data.append(i.toJSON())

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
        context['form_pro'] = ProductForm()
        context['form_buy'] = BuyForm()
        context['form_buy_detail'] = DetailBuyForm()
        context['list_url'] = reverse_lazy('cashier:buys')
        return context