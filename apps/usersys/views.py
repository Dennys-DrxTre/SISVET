from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse

from apps.entity.models import Client, Pet

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

    def get(self, request, *args, **kwargs):

        client = Client.objects.get(dni=request.user)
        pet = Pet.objects.filter(client=client)
        return render(request, self.template_name,{'obj':client, 'pet':pet})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
