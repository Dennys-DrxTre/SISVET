from django.forms import ModelForm, ModelChoiceField
from apps.entity.models import Client, Provider, Pet
from apps.cashier.models import VaccineDay, ChildProduct

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

class VaccineDayForm(ModelForm):
    product = ModelChoiceField(queryset=ChildProduct.objects.filter(stock__gt=0).order_by('-id'))

    class Meta:
        model = VaccineDay
        fields = '__all__'