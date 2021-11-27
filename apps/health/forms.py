from django.forms import ModelForm
from apps.health.models import Consultation, Vaccine, Parasite

class ConsultaForm(ModelForm):

    class Meta:
        model = Consultation
        fields = '__all__'

class DesparacitacionForm(ModelForm):

    class Meta:
        model = Parasite
        fields = '__all__'

class VacunaForm(ModelForm):

    class Meta:
        model = Vaccine
        fields = '__all__'
