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

from apps.entity.forms import PetForm
from apps.entity.models import Pet, Client
from apps.health.models import Consultation, Parasite, Vaccine

from apps.entity.mixins import Perms_Check

# CRUD PETS URL
class PetViews(Perms_Check, TemplateView):
    template_name = 'pet/pets.html'
    permission_required = 'entity.view_pet'

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
                for i in Pet.objects.all():
                    if i.status == True:
                        i.status = '<span class="badge badge-success btn-colores">Activado</span>'
                    else:
                        i.status = '<span class="badge badge-dark">Desactivado</span>'
                    data.append(i.toJSON())
            
            elif action == 'add':
                perms = ('entity.add_pet',)
                if request.user.has_perms(perms):
                    pet = Pet()
                    pet.name = request.POST.get('name')
                    pet.date_nac = request.POST.get('date_nac')
                    pet.gender = request.POST.get('gender')
                    pet.race = request.POST.get('race')
                    pet.weight = request.POST.get('weight')
                    pet.specie = request.POST.get('specie')
                    pet.date_up = request.POST.get('date_up')
                    pet.substitute = request.POST.get('substitute')
                    pet.client = Client.objects.get(pk = request.POST.get('client'))
                    pet.status = 'status' in request.POST
                    pet.save()
                else:
                    data['error'] = 'No tiene permisos para registrar una mascota'
            
            elif action == 'edit':
                perms = ('entity.change_pet',)
                if request.user.has_perms(perms):
                    pet = Pet.objects.get(pk=request.POST['id'])
                    pet.name = request.POST.get('name')
                    pet.date_nac = request.POST.get('date_nac')
                    pet.gender = request.POST.get('gender')
                    pet.race = request.POST.get('race')
                    pet.weight = request.POST.get('weight')
                    pet.specie = request.POST.get('specie')
                    pet.date_up = request.POST.get('date_up')
                    pet.substitute = request.POST.get('substitute')
                    pet.client = Client.objects.get(pk=request.POST.get('client'))
                    pet.status = 'status' in request.POST
                    pet.save()
                else:
                    data['error'] = 'No tiene permisos para editar una mascota'      

            elif action == 'delete':
                perms = ('entity.delete_pet',)
                if request.user.has_perms(perms):
                    pet = Pet.objects.get(pk=request.POST['id'])            
                    pet.delete()
                else:
                    data['error'] = 'No tiene permisos para eliminar una mascota'
            
            elif action == 'btn-estado':
                perms = ('entity.change_pet',)
                if request.user.has_perms(perms):
                    pet = Pet.objects.get(pk=request.POST['id'])
                    if pet.status:
                        pet.status = False
                        pet.save()
                    else:
                        pet.status = True
                        pet.save()
                else:
                    data['error'] = 'No tiene permisos para editar una mascota'  

            else:
                data['error'] = 'Ha ocurrido un error'           

        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'SISVET | Listado de Mascotas'
        context['sub_titulo'] = 'Listado de Mascotas'
        context['navegacion'] = 'Mascotas'
        context['form'] = PetForm()
        context['list_url'] = reverse_lazy('entity:pets')
        return context


def detail_pet(request, id):
    template_name = 'pet/detail_pet.html'
    context = {}

    if id:
        pet = Pet.objects.filter(pk = id).first()
        consult = Consultation.objects.filter(pet_id = id).order_by('-id')[:15]
        parasite = Parasite.objects.filter(pet_id = id).order_by('-id')[:15]
        vaccine = Vaccine.objects.filter(pet_id = id).order_by('-id')[:15]

        context = {
            'pet': pet,
            'consult': consult,
            'parasite': parasite,
            'vaccine': vaccine,
        }

    else:
        context = {
            'prod': 'No hay datos',
            'stock': 'No hay datos'
        }

    return render(request, template_name, context)