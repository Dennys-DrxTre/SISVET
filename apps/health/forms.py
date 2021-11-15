from django.forms import ModelForm
from apps.health.models import Consultation, Vaccine, Parasite

class ConsultForm(ModelForm):

    class Meta:
        model = Consultation
        fields = '__all__'

        

