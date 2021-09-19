from django.forms import ModelForm
from apps.entity.models import Client, Provider, Pet

class ClientForm(ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

        

class ProviderForm(ModelForm):

    class Meta:
        model = Provider
        fields = '__all__'

class PetForm(ModelForm):

    class Meta:
        model = Pet
        fields = '__all__'