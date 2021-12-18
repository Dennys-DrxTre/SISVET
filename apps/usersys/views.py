import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from CONFIG import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from datetime import date
from apps.entity.mixins import Perms_Check
from django.urls import reverse_lazy
from tablib import Dataset
from django.contrib import messages


from apps.entity.models import Client, Pet
from apps.health.models import Consultation
from apps.usersys.models import NotificationStatus

from .resources import ClientResource, PetResource, ProviderResource, ConsultationResource, VaccineResource, ParasiteResource, VaccineDayResource, Det_VaccineDayResource, ProductResource, ChildProductResource, Buy_SaleResource, Detail_BSResource

# Create your views here.
class LoginFormView(LoginView):
    template_name = 'user/login.html'

    def dispatch(self, request, *args, **kwargs):

        if not Permission.objects.filter(codename='view_clientuser'):
            content_type = ContentType.objects.get_for_model(Client)
            print(content_type)
            permission = Permission.objects.create(
                codename='view_clientuser',
                name='Can View ClientUser',
                content_type=content_type,
            )            

        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request,*args, **kwargs) 

class ClientUser(TemplateView):
    template_name = "user/clientuser.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        client = Client.objects.get(dni=request.user)
        pet = Pet.objects.filter(client=client)
        return render(request, self.template_name,{'obj':client, 'pet':pet})

def send_email_consult_and_email():
    try:
        query = NotificationStatus.objects.get(pk=1)
        if query.status:
            # CONEXION
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            for c in Consultation.objects.filter(status_notify = True):
                date_today = date.today()
<<<<<<< HEAD
                if c.pet.client.Email:
                    if c.date_u == date_today:
                        # cambiar estado
                        c.status_notify = False
                        c.save()
                        # Construimos el mensaje simple
                        mensaje = MIMEMultipart()
                        mensaje['From']= settings.EMAIL_HOST_USER
                        mensaje['To']= str(c.pet.client.Email) 
                        mensaje['Subject']="Tu mascota tiene una cita"

                        content = render_to_string('send_email.html', {'client': c})

                        mensaje.attach(MIMEText(content, 'html'))
                        # Envio del mensaje
                        mailServer.sendmail(settings.EMAIL_HOST_USER,str(c.pet.client.Email), mensaje.as_string())
                    else:
                        continue
=======
                if c.date_u == date_today:
                    # cambiar estado
                    c.status_notify = False
                    c.save()
                    # Construimos el mensaje simple
                    mensaje = MIMEMultipart()
                    mensaje['From']= settings.EMAIL_HOST_USER
                    mensaje['To']= str(c.pet.client.Email) 
                    mensaje['Subject']="Tu mascota tiene una cita"

                    content = render_to_string('send_email.html', {'client': c})

                    mensaje.attach(MIMEText(content, 'html'))
                    # Envio del mensaje
                    mailServer.sendmail(settings.EMAIL_HOST_USER,str(c.pet.client.Email), mensaje.as_string())
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5
                else:
                    continue
        
    except Exception as e:
        print(e)

class Menu_Notification(Perms_Check, TemplateView):
    template_name = 'user/menu_noti.html'
<<<<<<< HEAD
    permission_required = 'usersys.view_notificationstatus'
=======
    permission_required = 'cashier.view_detail_bs'
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'active':
                query = NotificationStatus.objects.get(pk=1)
                query.status = True
                data = query.status
                query.save()
            elif action == 'inactive':
                query = NotificationStatus.objects.get(pk=1)
                query.status = False
                data = query.status
                query.save()
            else:
                data['error'] = 'Ha ocurrido un error'
                
        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def status_consult(self):
        query = NotificationStatus.objects.get(pk=1)
        return query.status
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = ''
        
        context['status'] = self.status_consult()
        return context

class BackupViews(Perms_Check, TemplateView):
    template_name = 'user/backup_menu.html'
<<<<<<< HEAD
    permission_required = 'usersys.view_notificationstatus'
=======
    permission_required = 'cashier.view_detail_bs'
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_client(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            client_resource = ClientResource()
            dataset = client_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Clientes-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')
   
@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_client(request, *args, **kwargs):
    template_name = 'imports/import_client.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                client_resource = ClientResource()
                dataset = Dataset()
                new_clients = request.FILES['myfile']

                imported_data = dataset.load(new_clients.read())
                result = client_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    client_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_pet(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            pet_resource = PetResource()
            dataset = pet_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Mascotas-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_pet(request, *args, **kwargs):
    template_name = 'imports/import_pet.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                pet_resource = PetResource()
                dataset = Dataset()
                new_pets = request.FILES['myfile']

                imported_data = dataset.load(new_pets.read())
                result = pet_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    pet_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_provider(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            provider_resource = ProviderResource()
            dataset = provider_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Proveedores-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_provider(request, *args, **kwargs):
    template_name = 'imports/import_provider.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                provider_resource = ProviderResource()
                dataset = Dataset()
                new_providers = request.FILES['myfile']

                imported_data = dataset.load(new_providers.read())
                result = provider_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    provider_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_consult(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            consult_resource = ConsultationResource()
            dataset = consult_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Consultas-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_consult(request, *args, **kwargs):
    template_name = 'imports/import_consult.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                consult_resource = ConsultationResource()
                dataset = Dataset()
                new_consults = request.FILES['myfile']

                imported_data = dataset.load(new_consults.read())
                result = consult_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    consult_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_vaccine(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            vaccine_resource = VaccineResource()
            dataset = vaccine_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Vacunaciones-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_vaccine(request, *args, **kwargs):
    template_name = 'imports/import_vaccine.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                vaccine_resource = VaccineResource()
                dataset = Dataset()
                new_vaccines = request.FILES['myfile']

                imported_data = dataset.load(new_vaccines.read())
                result = vaccine_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    vaccine_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_parasite(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            parasite_resource = ParasiteResource()
            dataset = parasite_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Desparsitaciones-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_parasite(request, *args, **kwargs):
    template_name = 'imports/import_parasite.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                parasite_resource = ParasiteResource()
                dataset = Dataset()
                new_parasites = request.FILES['myfile']

                imported_data = dataset.load(new_parasites.read())
                result = parasite_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    parasite_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_vaccineday(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            vaccineday_resource = VaccineDayResource()
            dataset = vaccineday_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Jornada_Vacunacion-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_vaccineday(request, *args, **kwargs):
    template_name = 'imports/import_vaccineday.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                vaccineday_resource = VaccineDayResource()
                dataset = Dataset()
                new_vaccinedays = request.FILES['myfile']

                imported_data = dataset.load(new_vaccinedays.read())
                result = vaccineday_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    vaccineday_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_det_vaccineday(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            det_vaccineday_resource = Det_VaccineDayResource()
            dataset = det_vaccineday_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Detalle_Jornada_Vacunacion-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_det_vaccineday(request, *args, **kwargs):
    template_name = 'imports/import_det_vaccineday.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                det_vaccineday_resource = Det_VaccineDayResource()
                dataset = Dataset()
                new_det_vaccinedays = request.FILES['myfile']

                imported_data = dataset.load(new_det_vaccinedays.read())
                result = det_vaccineday_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    det_vaccineday_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_product(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            product_resource = ProductResource()
            dataset = product_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Producto-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_product(request, *args, **kwargs):
    template_name = 'imports/import_product.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                product_resource = ProductResource()
                dataset = Dataset()
                new_products = request.FILES['myfile']

                imported_data = dataset.load(new_products.read())
                result = product_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    product_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_child_product(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            child_product_resource = ChildProductResource()
            dataset = child_product_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Child_Producto-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_child_product(request, *args, **kwargs):
    template_name = 'imports/import_child_product.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                child_product_resource = ChildProductResource()
                dataset = Dataset()
                new_child_products = request.FILES['myfile']

                imported_data = dataset.load(new_child_products.read())
                result = child_product_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    child_product_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_movement(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            movement_resource = Buy_SaleResource()
            dataset = movement_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Movimientos-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_movement(request, *args, **kwargs):
    template_name = 'imports/import_movement.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                movement_resource = Buy_SaleResource()
                dataset = Dataset()
                new_movements = request.FILES['myfile']

                imported_data = dataset.load(new_movements.read())
                result = movement_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    movement_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def export_det_movement(request):
    if request.user.is_authenticated:
        perms = ('cashier.change_buy_sale',)
        if request.user.has_perms(perms):
            date_r = date.today()
            det_movement_resource = Detail_BSResource()
            dataset = det_movement_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Detalle_Movimientos-{}.xlsx"'.format(date_r)
            return response
        else:
            messages.error(request, 'No tienes permisos')
            return redirect('usersys:menu_backup')
    else:
        messages.error(request, 'No estas autenticado')
        return redirect('usersys:login')

@login_required(redirect_field_name='dashboard:dashboard')
@permission_required('cashier.view_buy_sale', '/')
def import_det_movement(request, *args, **kwargs):
    template_name = 'imports/import_det_movement.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            perms = ('cashier.change_buy_sale',)
            if request.user.has_perms(perms):
                det_movement_resource = Detail_BSResource()
                dataset = Dataset()
                new_det_movements = request.FILES['myfile']

                imported_data = dataset.load(new_det_movements.read())
                result = det_movement_resource.import_data(dataset, dry_run=True)  # Test the data import
                if not result.has_errors():
                    det_movement_resource.import_data(dataset, dry_run=False)  # Actually import now
                    messages.success(request, 'Importacion Completa')
                    return redirect('usersys:menu_backup')
                else:
                    messages.error(request, 'Ha ocurrido un error')
            else:
                messages.error(request, 'No tienes permisos')
                return redirect('usersys:menu_backup')
        else:
            messages.error(request, 'No estas autenticado')
            return redirect('usersys:login')

    return render(request, template_name)