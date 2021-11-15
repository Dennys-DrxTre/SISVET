from django.db import models
from CONFIG.settings import MEDIA_URL
from datetime import datetime
from django.forms import model_to_dict
from apps.entity.choices import unidad_product, type_sale_buy
from apps.entity.models import Client, Provider, Estado, my_urlsecret
from apps.health.models import Consultation, Vaccine, Parasite
from django.db.models.signals import post_save
from django.db.models import Sum

# Create your models here.


class Product(Estado):
    name = models.CharField(max_length = 50, verbose_name='Nombre Producto')
    stock = models.IntegerField(default=0, verbose_name='Cantidad', null = True, blank=True)
    num_sales = models.IntegerField(default=0, verbose_name='Vendidos', null = True, blank=True )
    type_stock = models.CharField(max_length = 40, choices=unidad_product, verbose_name='Unidad Medida')
    quantity = models.FloatField(default=0, verbose_name='Cantidad de medidad', null = True, blank=True)

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'
        ordering = ['id']  
    
class ChildProduct(Estado):
    stock = models.IntegerField(default=0, verbose_name='Cantidad')
    price_buy = models.FloatField(default=0, verbose_name='Precio Compra')
    price_sale = models.FloatField(default=0, verbose_name='Precio Venta')
    date_conquered = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Vencimiento')
    profit = models.FloatField(default=0, verbose_name='Ganancia')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto', null = True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.product.name, self.date_conquered)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Cantidad_Productos'
        verbose_name = 'Cantidad_Producto'
        ordering = ['id'] 

    
class Buy_Sale(Estado):
    date = models.DateField(auto_now_add=True, verbose_name='Fecha')
    total = models.FloatField(default=0, verbose_name='Total')
    iva = models.FloatField(default=0, verbose_name='IVA')
    sub_total = models.FloatField(default=0, verbose_name='Sub Total')
    type_bs = models.CharField(max_length = 30, choices=type_sale_buy, verbose_name='Tipo')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente', null = True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Proveedor', null = True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_display_date(self):
        if self.date:
            return self.date.strftime("%d/%m/%Y")

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.get_display_date()
        if self.client:
            item['client'] = {'id':self.client.id, 'dni': self.client.type_name + self.client.dni}
        else:
            item['provider'] = {'id':self.provider.id, 'name': self.provider.name}
        return item

    class Meta:
        verbose_name_plural = 'Compras_Ventas'
        verbose_name = 'Compra_Venta'
        ordering = ['id']      
    
class Detail_BS(Estado):
    stock = models.IntegerField(default=0, verbose_name='Cantidad')
    total = models.FloatField(default=0, verbose_name='Total')
    profit = models.FloatField(default=0, verbose_name='Ganancia')
    buy_sale = models.ForeignKey(Buy_Sale, on_delete=models.CASCADE, verbose_name='Compra Venta', null = True, blank=True)
    product = models.ForeignKey(ChildProduct, on_delete=models.CASCADE, verbose_name='Producto', null = True, blank=True)
    
    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = {'id':self.product.id, 'name': self.product.product.name}
        return item

    class Meta:
        verbose_name_plural = 'Detalles_CV'
        verbose_name = 'Detalle_CV'
        ordering = ['id']  
    
      

def stock_product(sender, instance, **kwargs):                      
    cont = ChildProduct.objects.filter(product__name=instance.product.product.name).aggregate(Sum('stock'))
    prod_parent = Product.objects.get(pk = instance.product.product.id)
    prod_parent.stock = cont['stock__sum'] 
    prod_parent.save()

post_save.connect(stock_product, sender=Detail_BS)

