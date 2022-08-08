import os
from .models import *
from .serializers import *
from .permissions_enum import PermissionsEnum as permiso
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication

#Permissions
class PermissionsApi(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_USUARIO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_USUARIO.value)
        if view_perm or change_perm:
            permisos = Permission.objects.filter(content_type_id__gte=8).order_by('id')
            permisos_serializer = self.get_serializer(permisos, many=True)
            msg= 'No se encontraron registros de los permisos.'
            if(permisos_serializer.data):
                msg= 'Permisos encontrados.'
            return Response({'error': False, 'msg': msg, 'data': permisos_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene acceso para ver la lista de permisos.', 'data': None}, status = status.HTTP_403_FORBIDDEN)

#UsuariosAdmin
class UsuarioAdminApi(generics.ListCreateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        view_perm = request.user.has_perm(permiso.VIEW_USUARIO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_USUARIO.value)
        if view_perm or change_perm:
            usuarios = Usuario.objects.filter(is_staff=False).exclude(id = user_id)
            usuarios_serializer = self.get_serializer(usuarios, many=True)
            msg = 'No se han encontrado registros.'
            if(usuarios_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': usuarios_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_USUARIO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_USUARIO.value)
        usuario_serializer = self.get_serializer(data=request.data)
        if usuario_serializer.is_valid():
            user = usuario_serializer.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Cuenta de usuario registrada correctamente.', 'data': usuario_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Cuenta de usuario registrada correctamente.', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': usuario_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class UsuarioAdminDetailApi(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminSerializerPerfil
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Usuario, pk=self.kwargs.get('id'))
        except:
            return None

    def get(self, request, id=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_USUARIO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_USUARIO.value)
        if view_perm or change_perm:
            try:
                try:
                    usuario = Usuario.objects.get(id = id)
                    usuario_serializer = self.get_serializer(usuario)
                    #return Response({'error': False, 'msg': 'Usuario encontrado.', 'data': usuario_serializer.data}, status = status.HTTP_200_OK)
                    return Response(usuario_serializer.data, status = status.HTTP_200_OK)
                except Usuario.DoesNotExist:
                    return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id=None, *args, **kwargs):
        try:
            try:
                user = Usuario.objects.get(id = id)
                usuario_serializer = self.get_serializer(user, data=request.data)
                if usuario_serializer.is_valid():
                    user = usuario_serializer.save()
                    token = Token.objects.filter(user=user)
                    if(token):
                        user.auth_token.delete()
                    user.save()
                    return Response({'error': False,'msg': 'Perfil de usuario actualizado correctamente!!', 'data': usuario_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': usuario_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id=None, *args, **kwargs):
        try:
            try:
                usuario = Usuario.objects.get(id = id)
                if(str(usuario.avatar) != ''):
                    if os.path.isfile(usuario.avatar.path):
                        os.remove(usuario.avatar.path)
                usuario.delete()
                return Response({'error': False, 'msg': 'Usuario Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)
    
#UsuariosAdminCredentials
class UsuarioAdminCredentialsApi(generics.RetrieveUpdateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminSerializerCredentials
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Usuario, pk=self.kwargs.get('id'))
        except:
            return None

    def get(self, request, id=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_USUARIO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_USUARIO.value)
        if view_perm or change_perm:
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
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id=None, *args, **kwargs):
        try:
            try:
                user = Usuario.objects.get(id = id)
                usuario_serializer = self.get_serializer(user, data=request.data)
                if usuario_serializer.is_valid():
                    user = usuario_serializer.save()
                    token = Token.objects.filter(user=user)
                    if(token):
                        user.auth_token.delete()
                    pw = user.password
                    user.set_password(pw)
                    user.save()
                    return Response({'error': False,'msg': 'Credenciales de usuario actualizadas!!', 'data': usuario_serializer.data}, status=status.HTTP_200_OK)
                return Response({'error': True, 'msg': usuario_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Usuario.DoesNotExist:
                return Response({'error': True, 'msg': 'El usuario no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)