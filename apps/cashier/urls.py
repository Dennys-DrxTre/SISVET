from django.urls import path
from apps.cashier.views.product.views import ProductViews
from apps.cashier.views.buy.views import BuyViews, Create_Buy

app_name = 'cashier'

urlpatterns = [
    path('listado_products/', ProductViews.as_view(), name='products'),
    path('listado_compras/', BuyViews.as_view(), name='buys'),
    path('registro_compra/', Create_Buy.as_view(), name='buy'),


]