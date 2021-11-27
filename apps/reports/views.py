import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from xhtml2pdf import pisa
from django.utils import timezone

import datetime
from django.utils.dateparse import parse_date
from datetime import timedelta, date

from apps.entity.models import Pet
from apps.health.models import Parasite, Vaccine, Consultation
from apps.cashier.models import Buy_Sale, ChildProduct, Detail_BS, Product

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, "/media/"))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

# menu health
class MenuHealth(TemplateView):
    template_name = "health/menu_health.html"

class MenuCashier(TemplateView):
    template_name = "health/menu_cashier.html"

# MASCOTAS
def PetsReports(request):
    template_path= 'health/pets_reports.html'
    today = timezone.now()

    pet = Pet.objects.all()
    context = {
        'obj':pet,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_mascotas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# VACUNAS
def VaccineReports(request):
    template_path= 'health/vaccine_reports.html'
    today = timezone.now()

    vac = Vaccine.objects.all()
    context = {
        'obj':vac,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_vacunas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# Desparacitacion
def ParasiteReports(request):
    template_path= 'health/parasite_reports.html'
    today = timezone.now()

    par = Parasite.objects.all()
    context = {
        'obj':par,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_desparacitacion.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# CONSULTAS
def ConsultasReports(request):
    template_path= 'health/consultas_reports.html'
    today = timezone.now()

    consulta = Consultation.objects.all()
    context = {
        'obj':consulta,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_consultas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# CONSULTAS DETALLE
def ConsultaReports(request, id):
    template_path= 'health/Consulta_reports.html'

    mascota = Pet.objects.filter(id = id).first()
    consulta = Consultation.objects.filter(pet = mascota)
    desparasitacion = Parasite.objects.filter(pet = mascota)
    vacunacion = Vaccine.objects.filter(pet = mascota)

    today = timezone.now()

    context = {
        'consulta':consulta,
        'mascota': mascota,
        'despa': desparasitacion,
        'vacuna': vacunacion,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_consulta.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# VENTAS
def VentasReports(request):
    template_path= 'health/ventas_reports.html'
    today = timezone.now()

    ven = Buy_Sale.objects.filter(type_bs='Venta')
    context = {
        'obj':ven,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_ventas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# VENTAS DETALLE
def VentasDetalleReports(request, id):
    template_path= 'cashier/ventasDetalle_reports.html'
    today = timezone.now()

    ven = Detail_BS.objects.filter(buy_sale__id = id)
    context = {
        'obj':ven,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_ventasDetalle.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# COMPRA DETALLE
def CompraDetalleReports(request, id):
    template_path= 'cashier/CompraDetalle_reports.html'
    today = timezone.now()

    compra = Detail_BS.objects.filter(buy_sale__id = id)
    context = {
        'obj':compra,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_CompraDetalle.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# COMPRAS
def ComprasReports(request):
    template_path= 'cashier/compras_reports.html'
    today = timezone.now()

    com = Buy_Sale.objects.filter(type_bs='Compra')
    context = {
        'obj':com,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_compras.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# PRODUCTOS
def ProductosReports(request):
    template_path= 'cashier/products_reports.html'
    today = timezone.now()

    prod = Product.objects.all()
    context = {
        'obj':prod,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reportes_productos.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# REPORTES DINAMICOS

# CONSULTAS POR RANGO DE FECHAS
def Report_RangeDate(request, date1, date2):
    template_path = 'health/report_rangedate.html'
    today = date.today
    date1= parse_date(date1)
    date2= parse_date(date2)
    date2 = date2 + timedelta(days=1)

    date_range = Consultation.objects.filter(date_c__gte=date1, date_c__lt=date2)
    date2 = date2 - timedelta(days=1)

    context = {
        'obj': date_range,
        'f1': date1,
        'f2': date2,
        'today': today,
        'request': request,

    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Reporte por rango de fecha.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# VENTAS POR RANGO DE FECHAS
def Report_RangeDateVenta(request, date1, date2):
    template_path = 'cashier/report_rangedateventa.html'
    today = date.today
    date1= parse_date(date1)
    date2= parse_date(date2)
    date2 = date2 + timedelta(days=1)

    ven = Buy_Sale.objects.filter(type_bs='Venta').filter(date__gte=date1, date__lt=date2)
    date2 = date2 - timedelta(days=1)

    context = {
        'obj': ven,
        'f1': date1,
        'f2': date2,
        'today': today,
        'request': request,

    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Reporte por rango de fecha.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# COMPRAS POR RANGO DE FECHAS
def Report_RangeDateCompra(request, date1, date2):
    template_path = 'cashier/report_rangedateCompra.html'
    today = date.today
    date1= parse_date(date1)
    date2= parse_date(date2)
    date2 = date2 + timedelta(days=1)

    ven = Buy_Sale.objects.filter(type_bs='Compra').filter(date__gte=date1, date__lt=date2)
    date2 = date2 - timedelta(days=1)

    context = {
        'obj': ven,
        'f1': date1,
        'f2': date2,
        'today': today,
        'request': request,

    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Reporte por rango de fecha.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response