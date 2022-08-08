from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

#Obtener que tipo de autenticacion existe
FIELD_USERNAME = 'username'
def obtain_auth_type():
    field_username_or_email = ''
    for item in range(len(settings.NAME_USERNAME)):
        field_username_or_email = field_username_or_email + _(settings.NAME_USERNAME[item])
    return field_username_or_email

#Almacenamos el valor
FIELD_USERNAME = obtain_auth_type()

# Vista principal que retorna un mensaje de bienvenida y el tipo de autenticacion de nuestra api
class IndexView(APIView):
    http_method_names = ['get', 'options']
    
    def get(self, request, format=None):
        return Response({'msg': 'Bienevenido al desarrollo Full Stack', 'auth_type': FIELD_USERNAME.capitalize()}, status= status.HTTP_200_OK)