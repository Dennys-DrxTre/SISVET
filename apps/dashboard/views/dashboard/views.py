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
from apps.health.models import Consultation, Parasite, Vaccine

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

        # GANANCIA TOTAL
        sum_profit = Detail_BS.objects.filter(buy_sale__type_bs='Venta').aggregate(Sum('profit'))

        # LISTADO DE MODULOS [5]
        list_clients = Client.objects.all().order_by('-id')[0:5]
        list_pets = Pet.objects.all().order_by('-id')[0:5]
        list_buys = Buy_Sale.objects.filter(type_bs='Compra').order_by('-date')[0:5]
        list_sales = Buy_Sale.objects.filter(type_bs='Venta').order_by('-date')[0:5]

        context = {
            'count_sale': count_sale,
            'count_buy': count_buy,
            'count_client': count_client,
            'count_provider': count_provider,
            'count_pet': count_pet,
            'sum_profit': sum_profit['profit__sum'],
            'list_clients': list_clients,
            'list_pets': list_pets,
            'list_buys': list_buys,
            'list_sales': list_sales,

        }

        return render(request, self.template_name, context)

class ChartsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/charts.html'

    def dispatch(self, request, *args, **kwargs):
        perm = ('entity.view_clientuser',)
        if request.user.has_perms(perm):
            return HttpResponseRedirect(reverse_lazy('usersys:clientuser'))

        return super().dispatch(request, *args, **kwargs)

    def get (self, request,*args, **kwargs):

        # NUMERO DE VENTAS
        count_sales = Buy_Sale.objects.filter(type_bs='Venta').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()
        if len(count_sales) < (12):
            count_sales = Buy_Sale.objects.filter(type_bs='Venta').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()
        else:
            month_sale = len(count_sales) - int(12)
            count_sales = Buy_Sale.objects.filter(type_bs='Venta').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()[month_sale:]

        # NUMERO DE COMPRAS
        count_buys = Buy_Sale.objects.filter(type_bs='Compra').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()
        if len(count_buys) < (12):
            count_buys = Buy_Sale.objects.filter(type_bs='Compra').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()
        else:
            month_buy = len(count_buys) - int(12)
            count_buys = Buy_Sale.objects.filter(type_bs='Compra').annotate(month=TruncMonth('date')).values('month').annotate(cantidad=Count('id')).order_by()[month_buy:]

        # GANANCIAS MENSUALES
        count_profit = Detail_BS.objects.filter(buy_sale__type_bs='Venta').annotate(month=TruncMonth('buy_sale__date')).values('month').annotate(profit=Sum('profit')).order_by()
        if len(count_profit) < (12):
            count_profit = Detail_BS.objects.filter(buy_sale__type_bs='Venta').annotate(month=TruncMonth('buy_sale__date')).values('month').annotate(profit=Sum('profit')).order_by()
        else:
            month_profit = len(count_profit) - int(12)
            count_profit = Detail_BS.objects.filter(buy_sale__type_bs='Venta').annotate(month=TruncMonth('buy_sale__date')).values('month').annotate(profit=Sum('profit')).order_by()[month_profit:]

        # PRODUCTOS CON MENOR STOCK
        count_products = Product.objects.all().order_by('stock')[:8]

        # TOTAL DE VENTA, COMPRAS Y GANANCIAS POR MES ACTUAL
        profit_month = Detail_BS.objects.filter(buy_sale__type_bs='Venta').annotate(month=TruncMonth('buy_sale__date')).values('month').annotate(ganancias=Sum('profit')).order_by()
        profit_month_b = Buy_Sale.objects.filter(type_bs='Compra').annotate(month=TruncMonth('date')).values('month').annotate(ganancias=Sum('total')).order_by()
        profit_month_s = Buy_Sale.objects.filter(type_bs='Venta').annotate(month=TruncMonth('date')).values('month').annotate(ganancias=Sum('total')).order_by()

        # NUMERO DE CONSULTAS, DESPARASITACIONES Y VACUNACIONES
        count_consult = Consultation.objects.all()
        count_vaccine = Vaccine.objects.all()
        count_parasite = Parasite.objects.all()


        context = {

            'count_sales': count_sales,
            'count_buys': count_buys,
            'count_profit': count_profit,
            'count_products': count_products,
            'profit_month': profit_month,
            'profit_month_s': profit_month_s,
            'profit_month_b': profit_month_b,
            'count_consult': count_consult,
            'count_vaccine': count_vaccine,
            'count_parasite': count_parasite,
        }

        return render(request, self.template_name, context)