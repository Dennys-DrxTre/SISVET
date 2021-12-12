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
from django.contrib.auth.models import User, Permission
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction


from apps.entity.forms import VaccineDayForm
from apps.cashier.models import VaccineDay, Det_VaccineDay, ChildProduct
from apps.entity.models import Pet

from apps.entity.mixins import Perms_Check

# CRUD CLIENTS URL
class VaccineDayViews(Perms_Check, TemplateView):
    template_name = 'vaccine/vaccineday.html'
    permission_required = 'cashier.view_vaccineday'

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
                for i in VaccineDay.objects.all():
                    item = i.toJSON()
                    item['date'] = i.date.strftime("%d-%m-%Y")
                    item['type_stock'] = i.product.product.type_stock
                    data.append(item) 

            elif action == 'detail':
                data = []
                for i in Det_VaccineDay.objects.filter(vaccineday_id=request.POST['id']):
                    item = i.toJSON()
                    item['name'] = i.pet.name
                    item['client'] = i.pet.client.first_name
                    item['specie'] = i.pet.specie
                    item['type_stock'] = '{} {}'.format(int(i.quantity), i.vaccineday.product.product.type_stock) 
                    data.append(item)

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Jornadas de Vacunación'
        context['sub_titulo'] = 'Listado de Jornadas de Vacunación'
        context['navegacion'] = 'Jornada de Vacunación'
        context['list_url'] = reverse_lazy('health:vaccinedays')
        return context


class Create_VaccineDay(Perms_Check, SuccessMessageMixin, CreateView):
    template_name = 'vaccine/form_vaccineday.html'
    permission_required = 'cashier.change_vaccineday'
    model = VaccineDay
    form_class = VaccineDayForm
    success_massage = 'La jornada de vacunación ha sido registrada correctamente'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_pets':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                pets = Pet.objects.filter(name__icontains=request.POST['term']).filter(status=True).order_by('id')
                for i in pets.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    item['client'] = i.client.first_name
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 
                
                    vacc = VaccineDay()
                    vacc.description = vents['description']
                    vacc.date = vents['date']
                    vacc.quantity = int(vents['quantity'])
                    vacc.quantity_usage = int(vents['quantity_usage'])
                    vacc.quantity_pet = int(vents['quantity_for_pet'])  
                    vacc.product_id = vents['product']
                    prod = ChildProduct.objects.filter(pk = vacc.product_id).first()
                    prod.stock -= 1
                    prod.save()
                    vacc.save()

                    for i in vents['pets']:

                            det = Det_VaccineDay()
                            det.vaccineday_id = vacc.id
                            det.pet_id = i['id']
                            det.quantity = int(i['quantity'])
                            det.save() 

            else:
                data['error'] = 'Ha ocurrido un error'
                
        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Registar Jornada de Vacunación'
        context['sub_titulo'] = 'Registar Jornada de Vacunación'
        context['navegacion'] = 'Registar Jornada de Vacunación'
        context['navegacion2'] = 'Jornada de Vacunación'
        context['list_url'] = reverse_lazy('health:vaccinedays')
        context['action'] = 'add'
        context['det'] = []
        return context

class Edit_VaccineDay(Perms_Check, SuccessMessageMixin, UpdateView):
    template_name = 'vaccine/form_vaccineday.html'
    permission_required = 'cashier.change_vaccineday'
    model = VaccineDay
    form_class = VaccineDayForm
    success_massage = 'La venta ha sido modificada correctamente'


    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_pets':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                pets = Pet.objects.filter(name__icontains=request.POST['term']).filter(status=True).order_by('id')
                for i in pets.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    item['client'] = i.client.first_name
                    data.append(item)

            elif action == 'edit':
                with transaction.atomic():

                    vents = json.loads(request.POST['vents']) 
                
                    vacc = self.get_object()
                    vacc.description = vents['description']
                    vacc.date = vents['date']
                    vacc.quantity = int(vents['quantity'])
                    vacc.quantity_usage = int(vents['quantity_usage'])
                    vacc.quantity_pet = int(vents['quantity_for_pet'])  
                    prod1 = ChildProduct.objects.filter(pk = vacc.product_id).first()
                    prod1.stock += 1
                    prod1.save()
                    vacc.save()
                    vacc.product_id = vents['product']
                    prod = ChildProduct.objects.filter(pk = vacc.product_id).first()
                    prod.stock -= 1
                    prod.save()
                    vacc.save()

                    Det_VaccineDay.objects.filter(vaccineday = self.get_object()).delete()

                    for i in vents['pets']:

                            det = Det_VaccineDay()
                            det.vaccineday_id = vacc.id
                            det.pet_id = i['id']
                            det.quantity = int(i['quantity'])
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
            for i in Det_VaccineDay.objects.filter(vaccineday_id=self.get_object().id):
                item = i.pet.toJSON()
                item['quantity'] = i.quantity
                item['client'] = i.pet.client.first_name

                data.append(item)
        except:
            pass
        return data
    
    def get_date(self):
        data = []
        try:
            obj = VaccineDay.objects.filter(pk=self.get_object().id).first()
            item = obj.date
            data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Registar Jornada de Vacunación'
        context['sub_titulo'] = 'Registar Jornada de Vacunación'
        context['navegacion'] = 'Registar Jornada de Vacunación'
        context['navegacion2'] = 'Jornada de Vacunación'
        context['list_url'] = reverse_lazy('health:vaccinedays')
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
        context['date'] = json.dumps(self.get_date(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)

        return context