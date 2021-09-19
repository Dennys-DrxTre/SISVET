from django.db import models
from CONFIG.settings import MEDIA_URL
from datetime import datetime
from django.forms import model_to_dict
from apps.entity.choices import unidad_product, type_sale_buy
from apps.entity.models import Client, Provider, Estado, my_urlsecret
from apps.health.models import Consultation, Vaccine, Parasite
# Create your models here.


class Product(Estado):
    name = models.CharField(max_length = 50, verbose_name='Nombre Producto')
    stock = models.IntegerField(default=0, verbose_name='Cantidad')
    price_buy = models.FloatField(default=0, verbose_name='Precio Compra')
    price_sale = models.FloatField(default=0, verbose_name='Precio Venta')
    date_conquered = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Vencimiento')
    profit = models.FloatField(default=0, verbose_name='Ganancia')
    num_sales = models.IntegerField(default=0, verbose_name='Vendidos', null = True, blank=True )
    type_stock = models.CharField(max_length = 40, choices=unidad_product, verbose_name='Unidad Medida')
    quantity = models.FloatField(default=0, verbose_name='Cantidad de medidad')

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'
        ordering = ['id']   
    
    
class Buy_Sale(Estado):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Fecha')
    total = models.FloatField(default=0, verbose_name='Total')
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
            item['client'] = {'id':self.client.id, 'dni': self.client.dni}
        else:
            item['provider'] = {'id':self.provider.id, 'name': self.provider.name}
        return item

    class Meta:
        verbose_name_plural = 'Compras_Ventas'
        verbose_name = 'Compra_Venta'
        ordering = ['id']      
    
class Detail_BS(Estado):
    stock = models.IntegerField(default=0, verbose_name='Cantidad')
    price = models.FloatField(default=0, verbose_name='Precio')
    total = models.FloatField(default=0, verbose_name='Total')
    sub_total = models.FloatField(default=0, verbose_name='Sub Total')
    iva = models.FloatField(default=0, verbose_name='IVA')
    profit = models.FloatField(default=0, verbose_name='Ganancia')
    buy_sale = models.ForeignKey(Buy_Sale, on_delete=models.CASCADE, verbose_name='Compra Venta', null = True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto', null = True, blank=True)
    
    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Detalles_CV'
        verbose_name = 'Detalle_CV'
        ordering = ['id']  
    
      
    