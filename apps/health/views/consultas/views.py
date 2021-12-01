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
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User, Permission

from apps.health.forms import ConsultaForm
from apps.health.models import Consultation
from apps.entity.models import Pet
from apps.entity.mixins import Perms_Check

# CRUD CLIENTS URL
class ConsultaViews(Perms_Check, TemplateView):
    template_name = 'consultas/consultas.html'
    permission_required = 'health.view_consultation'

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
                for i in Consultation.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('health.add_consultation',)
                if request.user.has_perms(perms):
                    consul = Consultation()
                    consul.motive = request.POST.get('motive')
                    consul.symptom = request.POST.get('symptom')
                    consul.temperature = request.POST.get('temperature')
                    consul.total = request.POST.get('total')
                    consul.date_c = request.POST.get('date_c')
                    consul.date_u = request.POST.get('date_u')
                    consul.diag_pre = request.POST.get('diag_pre')
                    consul.diag_def = request.POST.get('diag_def')
                    consul.fre_car = request.POST.get('fre_car')
                    consul.fre_res = request.POST.get('fre_res')
                    consul.examination = request.POST.get('examination')
                    consul.pet = Pet.objects.get(pk = request.POST.get('pet'))
                    consul.status = 'status' in request.POST
                    consul.save()
                    
                else:
                    data['error'] = 'No tiene permisos para registrar una consulta'
            
            elif action == 'edit':
                perms = ('health.change_consultation',)
                if request.user.has_perms(perms):
                    consul = Consultation.objects.get(pk=request.POST['id'])
                    consul.motive = request.POST.get('motive')
                    consul.symptom = request.POST.get('symptom')
                    consul.temperature = request.POST.get('temperature')
                    consul.total = request.POST.get('total')
                    consul.date_c = request.POST.get('date_c')
                    consul.date_u = request.POST.get('date_u')
                    consul.diag_pre = request.POST.get('diag_pre')
                    consul.diag_def = request.POST.get('diag_def')
                    consul.fre_car = request.POST.get('fre_car')
                    consul.fre_res = request.POST.get('fre_res')
                    consul.examination = request.POST.get('examination')
                    consul.pet = Pet.objects.get(pk=request.POST.get('pet'))
                    consul.status = 'status' in request.POST
                    consul.save()

                else:
                    data['error'] = 'No tiene permisos para editar una consulta'      

            elif action == 'delete':
                perms = ('health.delete_consultation',)
                if request.user.has_perms(perms):
                    consul = Consultation.objects.get(pk=request.POST['id'])            
                    consul.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar una consulta'

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Consultas'
        context['sub_titulo'] = 'Listado de Consultas'
        context['navegacion'] = 'Consultas'
        context['form'] = ConsultaForm()
        context['list_url'] = reverse_lazy('health:consultas')
        return context