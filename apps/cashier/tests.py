from django.test import TestCase
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct
from django.db.models import Sum


# Create your tests here.

class ContadorStock(TestCase):

    def contador(self):
cont = ChildProduct.objects.filter(product__name='Correa').aggregate(Sum('stock'))
print(cont)    