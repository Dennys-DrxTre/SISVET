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

from apps.entity.forms import ClientForm
from apps.entity.models import Client, Pet

from apps.entity.mixins import Perms_Check

# CRUD CLIENTS URL
class ClientViews(Perms_Check, TemplateView):
    template_name = 'client/clients.html'
    permission_required = 'entity.view_client'

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
                for i in Client.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('entity.add_client',)
                if request.user.has_perms(perms):
                    clien = Client()
                    clien.type_name = request.POST.get('type_name')
                    clien.dni = request.POST.get('dni')
                    clien.first_name = request.POST.get('first_name')
                    clien.last_name = request.POST.get('last_name')
                    clien.gender = request.POST.get('gender')
                    clien.address = request.POST.get('address')
                    clien.Email = request.POST.get('Email')
                    clien.mobile = request.POST.get('mobile')
                    clien.tlf = request.POST.get('tlf')
                    clien.status = 'status' in request.POST
                    clien.save()
                    user = User.objects.create_user(clien.dni, clien.Email, clien.dni)
                    permission = Permission.objects.get(codename='view_clientuser')
                    user.user_permissions.add(permission)
                    print(user)
                    user.save()
                else:
                    data['error'] = 'No tiene permisos para registrar un cliente'
            
            elif action == 'edit':
                perms = ('entity.change_client',)
                if request.user.has_perms(perms):
                    clien = Client.objects.get(pk=request.POST['id'])
                    user = User.objects.get(username=clien.dni)
                    clien.type_name = request.POST.get('type_name')
                    clien.dni = request.POST.get('dni')
                    user.username = clien.dni
                    user.set_password(clien.dni)
                    user.save()
                    clien.first_name = request.POST.get('first_name')
                    clien.last_name = request.POST.get('last_name')
                    clien.gender = request.POST.get('gender')
                    clien.address = request.POST.get('address')
                    clien.Email = request.POST.get('Email')
                    clien.mobile = request.POST.get('mobile')
                    clien.tlf = request.POST.get('tlf')
                    clien.status = 'status' in request.POST
                    clien.save()

                else:
                    data['error'] = 'No tiene permisos para editar un cliente'      

            elif action == 'delete':
                perms = ('entity.delete_client',)
                if request.user.has_perms(perms):
                    clien = Client.objects.get(pk=request.POST['id'])
                    clien.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar un cliente'

            elif action == 'detail':
                data = []
                for i in Pet.objects.filter(client_id=request.POST['id']):
                    item = i.toJSON()
                    item['date_nac'] = i.date_nac.strftime("%d-%m-%Y")
                    data.append(item)


            elif action == 'btn-estado':
                perms = ('entity.change_client',)
                if request.user.has_perms(perms):
                    clien = Client.objects.get(pk=request.POST['id'])
                    if clien.status:
                        clien.status = False
                        clien.save()
                    else:
                        clien.status = True
                        clien.save()
                else:
                    data['error'] = 'No tiene permisos para editar un cliente'  

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Clientes'
        context['sub_titulo'] = 'Listado de Clientes'
        context['navegacion'] = 'Clientes'
        context['form'] = ClientForm()
        context['list_url'] = reverse_lazy('entity:clients')
        return context