from django.urls import path
from apps.usersys.views import LoginFormView, LogoutView, ClientUser

app_name = 'usersys'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientuser/', ClientUser.as_view(), name='clientuser'),
]

  