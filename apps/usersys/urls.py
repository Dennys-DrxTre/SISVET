from django.urls import path
from apps.usersys.views import LoginFormView, LogoutView, ClientUser, Menu_Notification, BackupViews, export_client, import_client, export_pet, import_pet, export_provider, import_provider, export_consult, import_consult, export_vaccine, import_vaccine, export_parasite, import_parasite, export_vaccineday, import_vaccineday, export_det_vaccineday, import_det_vaccineday, export_product, import_product, export_child_product, import_child_product, export_movement, import_movement, export_det_movement, import_det_movement

app_name = 'usersys'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientuser/', ClientUser.as_view(), name='clientuser'),
    path('menu_noficaciones/', Menu_Notification.as_view(), name='menu_noti'),
    path('menu_respaldo_datos/', BackupViews.as_view(), name='menu_backup'),

    # EXPORTS
    path('export_client/', export_client, name='exp_client'),
    path('export_pet/', export_pet, name='exp_pet'),
    path('export_provider/', export_provider, name='exp_provider'),
    path('export_consult/', export_consult, name='exp_consult'),
    path('export_vaccine/', export_vaccine, name='exp_vaccine'),
    path('export_parasite/', export_parasite, name='exp_parasite'),
    path('export_vaccineday/', export_vaccineday, name='exp_vaccineday'),
    path('export_det_vaccineday/', export_det_vaccineday, name='exp_det_vaccineday'),
    path('export_product/', export_product, name='exp_product'),
    path('export_child_product/', export_child_product, name='exp_child_product'),
    path('export_movement/', export_movement, name='exp_movement'),
    path('export_det_movement/', export_det_movement, name='exp_det_movement'),

    # IMPORTS
    path('import_client/', import_client, name='imp_client'),
    path('import_pet/', import_pet, name='imp_pet'),
    path('import_provider/', import_provider, name='imp_provider'),
    path('import_consult/', import_consult, name='imp_consult'),
    path('import_vaccine/', import_vaccine, name='imp_vaccine'),
    path('import_parasite/', import_parasite, name='imp_parasite'),
    path('import_vaccineday/', import_vaccineday, name='imp_vaccineday'),
    path('import_det_vaccineday/', import_det_vaccineday, name='imp_det_vaccineday'),
    path('import_product/', import_product, name='imp_product'),
    path('import_child_product/', import_child_product, name='imp_child_product'),
    path('import_movement/', import_movement, name='imp_movement'),
    path('import_det_movement/', import_det_movement, name='imp_det_movement'),

]

  