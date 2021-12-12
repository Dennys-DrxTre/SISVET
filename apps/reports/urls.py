from django.urls import path
from .views import PetsReports, VaccineReports, ParasiteReports, MenuHealth,MenuCashier, VentasReports, ConsultaReports
from .views import ConsultasReports, ProductosReports, ComprasReports, VentasDetalleReports, CompraDetalleReports, Report_RangeDate
from .views import Report_RangeDateVenta, Report_RangeDateCompra
from .views import ConsultaDetalleReports, VacunaDetalleReports, DespaDetalleReports

app_name = 'reports'

urlpatterns = [
    #MODULO HEALTH
    path("reports/pets/", PetsReports, name="report_pet"),
    path("reports/vaccine/", VaccineReports, name="report_vaccine"),
    path("reports/parasite/", ParasiteReports, name="report_parasite"),
    path("reports/consultation/<int:id>/", ConsultaReports, name="report_consultation"),
    path("reports/consultation/", ConsultasReports, name="report_consultas"),
    # MENU
    path("menu/reportes/medica/", MenuHealth.as_view(), name="menu_health"),
    path("menu/reportes/movimientos/", MenuCashier.as_view(), name="menu_cashier"),
    #MODULO CASHIER
    path("reports/ventas/", VentasReports, name="report_ventas"),
    path("reports/ventas/<int:id>/", VentasDetalleReports, name="report_ventasDetalle"),
    path("reports/compras/", ComprasReports, name="report_compras"),
    path("reports/compras/<int:id>/", CompraDetalleReports, name="report_CompraDetalle"),
    path("reports/productos/", ProductosReports, name="report_productos"),
    # REPORTES DINAMICOS
    path("reports_dinamic/<str:date1>/<str:date2>", Report_RangeDate, name="report_rangoConsulta"),
    path("reports_dinamic/venta/<str:date1>/<str:date2>", Report_RangeDateVenta, name="report_rangoVenta"),
    path("reports_dinamic/compra/<str:date1>/<str:date2>", Report_RangeDateCompra, name="report_rangoVenta"),

    # REPORTES DETALLES SECCION MEDICA
    path("reports/consultation/detalle/<int:id>/", ConsultaDetalleReports, name="report_consultationD"),
    path("reports/vacunacion/detalle/<int:id>/", VacunaDetalleReports, name="report_vaccinateD"),
    path("reports/desparasitacion/detalle/<int:id>/", DespaDetalleReports, name="report_desparasitationD"),
]
