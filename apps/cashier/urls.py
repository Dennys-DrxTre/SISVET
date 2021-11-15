from django.urls import path
from apps.cashier.views.product.views import ProductViews, detail_product
from apps.cashier.views.buy.views import BuyViews, Create_Buy, Edit_Buy
from apps.cashier.views.sale.views import SaleViews, Create_Sale, Edit_Sale


app_name = 'cashier'

urlpatterns = [
    path('listado_products/', ProductViews.as_view(), name='products'),
    path('listado_products/detail/<int:id>/', detail_product, name='product_detail'),
    path('listado_compras/', BuyViews.as_view(), name='buys'),
    path('registro_compra/', Create_Buy.as_view(), name='buy'),
    path('editar_compra/<int:pk>/', Edit_Buy.as_view(), name='buy_edit'),
    path('listado_ventas/', SaleViews.as_view(), name='sales'),
    path('registro_venta/', Create_Sale.as_view(), name='sale'),
    path('editar_venta/<int:pk>/', Edit_Sale.as_view(), name='sale_edit'),
    

]