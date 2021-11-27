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
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Permission

from apps.health.forms import VacunaForm
from apps.health.models import Vaccine
from apps.entity.models import Pet

from apps.entity.mixins import Perms_Check

# CRUD DESPARACITACION URL
class VacunaViews(Perms_Check, TemplateView):
    template_name = 'vacunacion/vacunacion.html'
    permission_required = 'health.view_vaccine'

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
                for i in Vaccine.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('health.add_vaccine',)
                if request.user.has_perms(perms):
                    vacu = Vaccine()
                    vacu.name = request.POST.get('name')
                    vacu.description = request.POST.get('description')
                    vacu.total = request.POST.get('total')
                    vacu.date = request.POST.get('date')
                    vacu.new_date = datetime.strptime(vacu.date, '%Y-%m-%d') + timedelta(days = 30)
                    vacu.pet = Pet.objects.get(pk = request.POST.get('pet'))
                    vacu.status = 'status' in request.POST
                    vacu.save()
                    
                else:
                    data['error'] = 'No tiene permisos para registrar una consulta'
            
            elif action == 'edit':
                perms = ('health.change_vaccine',)
                if request.user.has_perms(perms):
                    vacu = Vaccine.objects.get(pk=request.POST['id'])
                    vacu.name = request.POST.get('name')
                    vacu.description = request.POST.get('description')
                    vacu.total = request.POST.get('total')
                    vacu.date = request.POST.get('date')
                    vacu.pet = Pet.objects.get(pk=request.POST.get('pet'))
                    vacu.status = 'status' in request.POST
                    vacu.save()

                else:
                    data['error'] = 'No tiene permisos para editar una consulta'      

            elif action == 'delete':
                perms = ('health.delete_vaccine',)
                if request.user.has_perms(perms):
                    vacu = Vaccine.objects.get(pk=request.POST['id'])            
                    vacu.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar una consulta'

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Vacunas'
        context['sub_titulo'] = 'Listado de Vacunas'
        context['navegacion'] = 'Vacunas'
        context['form'] = VacunaForm()
        context['list_url'] = reverse_lazy('health:vacunas')
        return context