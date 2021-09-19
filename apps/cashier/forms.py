from django.forms import ModelForm
from apps.cashier.models import Product, Buy_Sale, Detail_BS

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class BuyForm(ModelForm):

    class Meta:
        model = Buy_Sale
        fields = '__all__'

class DetailBuyForm(ModelForm):

    class Meta:
        model = Detail_BS
        fields = '__all__'