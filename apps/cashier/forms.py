from django.forms import ModelForm
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct
from apps.usersys.models import DollarStatus

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class Product_Stock_Form(ModelForm):

    class Meta:
        model = ChildProduct
        fields = '__all__'

class BuyForm(ModelForm):

    class Meta:
        model = Buy_Sale
        fields = '__all__'

class DetailBuyForm(ModelForm):

    class Meta:
        model = Detail_BS
        fields = '__all__'

class DollarForm(ModelForm):

    class Meta:
        model = DollarStatus
        fields = '__all__'