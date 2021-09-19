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

from apps.entity.forms import ProviderForm
from apps.entity.models import Provider

from apps.entity.mixins import Perms_Check

# CRUD PROVIDERS URL
class ProviderViews(Perms_Check, TemplateView):
    template_name = 'provider/providers.html'
    permission_required = 'entity.view_provider'

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
                for i in Provider.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('entity.add_provider',)
                if request.user.has_perms(perms):
                    prov = Provider()
                    prov.name = request.POST.get('name')
                    prov.rif = request.POST.get('rif')
                    prov.Email = request.POST.get('Email')
                    prov.mobile = request.POST.get('mobile')
                    prov.tlf = request.POST.get('tlf')
                    prov.status = 'status' in request.POST
                    prov.save()
                else:
                    data['error'] = 'No tiene permisos para registrar un proveedor'
            
            elif action == 'edit':
                perms = ('entity.change_provider',)
                if request.user.has_perms(perms):
                    prov = Provider.objects.get(pk=request.POST['id'])
                    prov.name = request.POST.get('name')
                    prov.rif = request.POST.get('rif')
                    prov.Email = request.POST.get('Email')
                    prov.mobile = request.POST.get('mobile')
                    prov.tlf = request.POST.get('tlf')
                    prov.status = 'status' in request.POST
                    prov.save()
                else:
                    data['error'] = 'No tiene permisos para editar un proveedor'      

            elif action == 'delete':
                perms = ('entity.delete_provider',)
                if request.user.has_perms(perms):
                    prov = Provider.objects.get(pk=request.POST['id'])            
                    prov.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar un proveedor'
            
            elif action == 'btn-estado':
                perms = ('entity.change_provider',)
                if request.user.has_perms(perms):
                    prov = Provider.objects.get(pk=request.POST['id'])
                    if prov.status:
                        prov.status = False
                        prov.save()
                    else:
                        prov.status = True
                        prov.save()
                else:
                    data['error'] = 'No tiene permisos para editar un proveedor'  

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Proveedores'
        context['sub_titulo'] = 'Listado de Proveedores'
        context['navegacion'] = 'Proveedores'
        context['form'] = ProviderForm()
        context['list_url'] = reverse_lazy('entity:providers')
        return context