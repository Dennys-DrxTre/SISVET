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

from apps.health.forms import DesparacitacionForm
from apps.health.models import Parasite
from apps.entity.models import Pet

from apps.entity.mixins import Perms_Check

# CRUD DESPARACITACION URL
class DesparacitacionViews(Perms_Check, TemplateView):
    template_name = 'desparacitacion/desparacitacion.html'
    permission_required = 'health.view_parasite'

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
                for i in Parasite.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('health.add_parasite',)
                if request.user.has_perms(perms):
                    para = Parasite()
                    para.name = request.POST.get('name')
                    para.description = request.POST.get('description')
                    para.total = request.POST.get('total')
                    para.date = request.POST.get('date')
                    para.new_date = datetime.strptime(para.date, '%Y-%m-%d') + timedelta(days = 30)
                    para.pet = Pet.objects.get(pk = request.POST.get('pet'))
                    para.status = 'status' in request.POST
                    para.save()
                    
                else:
                    data['error'] = 'No tiene permisos para registrar una consulta'
            
            elif action == 'edit':
                perms = ('health.change_parasite',)
                if request.user.has_perms(perms):
                    para = Parasite.objects.get(pk=request.POST['id'])
                    para.name = request.POST.get('name')
                    para.description = request.POST.get('description')
                    para.total = request.POST.get('total')
                    para.date = request.POST.get('date')
                    para.pet = Pet.objects.get(pk=request.POST.get('pet'))
                    para.status = 'status' in request.POST
                    para.save()

                else:
                    data['error'] = 'No tiene permisos para editar una consulta'      

            elif action == 'delete':
                perms = ('health.delete_parasite',)
                if request.user.has_perms(perms):
                    para = Parasite.objects.get(pk=request.POST['id'])            
                    para.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar una consulta'

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Desparasitacion'
        context['sub_titulo'] = 'Listado de Desparasitacion'
        context['navegacion'] = 'Desparasitacion'
        context['form'] = DesparacitacionForm()
        context['list_url'] = reverse_lazy('health:desparacitacion')
        return context