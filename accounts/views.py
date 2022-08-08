from .serializers import *
from users.models import *
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from authentication.views import succes_response

class ProfileView(generics.RetrieveUpdateAPIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UsuarioSerializer
    http_method_names = ['get', 'put', 'options']
    
    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user

class UserDetailApi(generics.RetrieveUpdateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializerPerfil
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Usuario, pk=self.kwargs.get('id'))
        except:
            return None
    def get(self, request, id=None, *args, **kwars):
        try:
            try:
                user = Usuario.objects.get(id = id)
                user_serializer = self.get_serializer(user)
                #token = Token.objects.get(user = user)
                #return succes_response('Perfil de usuario!!', token, user_serializer, user, status.HTTP_200_OK)
                return Response(user_serializer.data, status = status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def put(self, request, id=None, *args, **kwargs):
        try:
            try:
                user = Usuario.objects.get(id = id)
                updateUser = UsuarioSerializerPerfil(user, data=request.data)
                if updateUser.is_valid():
                    user = updateUser.save()
                    user.save()
                    user_serializer = self.get_serializer(user)
                    token, created = Token.objects.get_or_create(user=user)
                    return succes_response('Cuenta actualizada correctamente!!', token, user_serializer, user, status.HTTP_200_OK)
                return Response({'error': True, 'msg': updateUser.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class UserUpdateCredentials(generics.RetrieveUpdateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializerCredentials
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Usuario, pk=self.kwargs.get('id'))
        except:
            return None
    def get(self, request, id=None, *args, **kwars):
        try:
            try:
                user = Usuario.objects.get(id = id)
                user_serializer = self.get_serializer(user)
                #return Response({'error': False, 'msg': 'Actualizar credenciales de usuario.', 'data': user_serializer.data}, status = status.HTTP_200_OK)
                return Response(user_serializer.data, status = status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def put(self, request, id=None, *args, **kwargs):
        try:
            try:
                user = Usuario.objects.get(id = id)
                updateUser = UsuarioSerializerCredentials(user, data=request.data)
                if updateUser.is_valid():
                    user = updateUser.save()
                    pw = user.password
                    user.set_password(pw)
                    user.save()
                    user_serializer = self.get_serializer(user)
                    token, created = Token.objects.get_or_create(user=user)
                    return succes_response('Credenciales de usuario actualizadas correctamente!!', token, user_serializer, user, status.HTTP_200_OK)
                return Response({'error': True, 'msg': updateUser.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)