from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Avg
from django.db.models import Sum
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import Count
from datetime import datetime, date, time, timedelta
from django.utils.dateparse import parse_date

from apps.entity.models import Pet, Client, Provider
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        perm = ('entity.view_clientuser',)
        if request.user.has_perms(perm):
            return HttpResponseRedirect(reverse_lazy('usersys:clientuser'))

        return super().dispatch(request, *args, **kwargs)

    def get (self, request,*args, **kwargs):

        # CONTADOR DE OBJETOS (VENTAS, COMPRAS, CLIENTES, PROVEEDORES, MASCOTAS)
        count_sale = Buy_Sale.objects.filter(type_bs='Venta')
        count_buy = Buy_Sale.objects.filter(type_bs='Compra')
        count_client = Client.objects.all()
        count_provider = Provider.objects.all()
        count_pet = Pet.objects.all()

        sum_profit = Detail_BS.objects.filter(buy_sale__type_bs='Venta').aggregate(Sum('profit'))

        context = {
            'count_sale': count_sale,
            'count_buy': count_buy,
            'count_client': count_client,
            'count_provider': count_provider,
            'count_pet': count_pet,
            'sum_profit': sum_profit['profit__sum'],

        }

        return render(request, self.template_name, context)