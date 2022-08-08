import os
from .models import *
from .serializers import *
from myproject.selects import *
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from users.permissions_enum import PermissionsEnum as permiso

# Create your views here.
#Investigación
class ProyectoApi(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_PROYECTO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PROYECTO.value)
        if view_perm or change_perm:
            proyectos = Proyecto.objects.all()
            proyectos_serializer = self.get_serializer(proyectos, many=True)
            msg = 'No se han encontrado registros.'
            if(proyectos_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': proyectos_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_PROYECTO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PROYECTO.value)
        proyecto_serializer = self.get_serializer(data=request.data)
        if proyecto_serializer.is_valid():
            proyecto_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': proyecto_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': proyecto_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    
class ProyectoDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Proyecto, pk=self.kwargs.get('id_pro'))
        except:
            return None

    def get(self, request, id_pro=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_PROYECTO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PROYECTO.value)
        if view_perm or change_perm:
            try:
                try:
                    proyecto = Proyecto.objects.get(id_pro = id_pro)
                    proyecto_serializer = self.get_serializer(proyecto)
                    #return Response({'error': False, 'msg': 'Proyecto encontrado.', 'data': proyecto_serializer.data}, status = status.HTTP_200_OK)
                    return Response(proyecto_serializer.data, status = status.HTTP_200_OK)
                except Proyecto.DoesNotExist:
                    return Response({'error': True, 'msg': 'El proyecto no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_pro=None, *args, **kwargs):
        try:
            try:
                proyecto = Proyecto.objects.get(id_pro = id_pro)
                proyecto_serializer = self.get_serializer(proyecto, data=request.data)
                if proyecto_serializer.is_valid():
                    proyecto_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': proyecto_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': proyecto_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Proyecto.DoesNotExist:
                return Response({'error': True, 'msg': 'El proyecto no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_pro=None, *args, **kwargs):
        try:
            try:
                proyecto = Proyecto.objects.get(id_pro = id_pro)
                proyecto.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Proyecto.DoesNotExist:
                return Response({'error': True, 'msg': 'El proyecto no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicProyectoApi(generics.ListAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        proyectos = Proyecto.objects.all()
        proyectos_serializer = self.get_serializer(proyectos, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(proyectos_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': proyectos_serializer.data}, status = status.HTTP_200_OK)
           
class PublicProyectoDetailApi(generics.RetrieveAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_pro=None, *args, **kwars):
        try:
            try:
                proyecto = Proyecto.objects.get(id_pro = id_pro)
                proyecto_serializer = self.get_serializer(proyecto)
                return Response({'error': False, 'msg': 'Proyecto encontrado.', 'data': proyecto_serializer.data}, status = status.HTTP_200_OK)
            except Proyecto.DoesNotExist:
                return Response({'error': True, 'msg': 'El proyecto no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)


class ArchivoApi(generics.ListCreateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_ARCHIVO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARCHIVO.value)
        if view_perm or change_perm:
            archivos = Archivo.objects.all()
            archivos_serializer = self.get_serializer(archivos, many=True)
            msg = 'No se han encontrado registros.'
            if(archivos_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': archivos_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_ARCHIVO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARCHIVO.value)
        archivo_serializer = self.get_serializer(data=request.data)
        if archivo_serializer.is_valid():
            archivo_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Archivo subido correctamente.', 'data': archivo_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Archivo subido correctamente.', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': archivo_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class ArchivoDetailApi(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Archivo, pk=self.kwargs.get('id_arch'))
        except:
            return None

    def get(self, request, id_arch=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_ARCHIVO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARCHIVO.value)
        if view_perm or change_perm:
            try:
                try:
                    archivo = Archivo.objects.get(id_arch = id_arch)
                    archivo_serializer = self.get_serializer(archivo)
                    #return Response({'error': False, 'msg': 'Archivo encontrado.', 'data': archivo_serializer.data}, status = status.HTTP_200_OK)
                    return Response(archivo_serializer.data, status = status.HTTP_200_OK)
                except Archivo.DoesNotExist:
                    return Response({'error': True, 'msg': 'El archivo no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_arch=None, *args, **kwargs):
        try:
            try:
                archivo = Archivo.objects.get(id_arch = id_arch)
                archivo_serializer = self.get_serializer(archivo, data=request.data)
                if archivo_serializer.is_valid():
                    archivo_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': archivo_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': archivo_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Archivo.DoesNotExist:
                return Response({'error': True, 'msg': 'El archivo no existe', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_arch=None, *args, **kwargs):
        try:
            try:
                archivo = Archivo.objects.get(id_arch = id_arch)
                if(str(archivo.archivo_arch) != ''):
                    if os.path.isfile(archivo.archivo_arch.path):
                        os.remove(archivo.archivo_arch.path)
                archivo.delete()
                return Response({'error': False, 'msg': 'Archivo Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Archivo.DoesNotExist:
                return Response({'error': True, 'msg': 'El archivo no existe'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido'}, status = status.HTTP_400_BAD_REQUEST)

class ArchivoByProApi(generics.ListAPIView):
    parser_class = (FileUploadParser,)
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'options']

    def get(self, request, fk_id_pro=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_ARCHIVO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARCHIVO.value)
        if view_perm or change_perm:
            try:
                archivos = Archivo.objects.filter(fk_id_pro = fk_id_pro)
                archivos_serializer = self.get_serializer(archivos, many=True)
                msg = 'Este proyecto no tiene archivos vinculados.'
                if(archivos_serializer.data):
                    msg = 'Archivos encontrados.'
                return Response({'error': False, 'msg': msg, 'data': archivos_serializer.data}, status = status.HTTP_200_OK)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los archivos del proyecto.', 'data': None}, status = status.HTTP_200_OK)

#Publicaciones
class ArticuloApi(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_ARTICULO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARTICULO.value)
        if view_perm or change_perm:
            articulos = Articulo.objects.all()
            articulos_serializer = self.get_serializer(articulos, many=True)
            msg = 'No se han encontrado registros.'
            if(articulos_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': articulos_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_ARTICULO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARTICULO.value)
        articulo_serializer = self.get_serializer(data=request.data)
        if articulo_serializer.is_valid():
            articulo_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': articulo_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': articulo_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class ArticuloDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Articulo, pk=self.kwargs.get('id_art'))
        except:
            return None

    def get(self, request, id_art=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_ARTICULO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_ARTICULO.value)
        if view_perm or change_perm:
            try:
                try:
                    articulo = Articulo.objects.get(id_art = id_art)
                    articulo_serializer = self.get_serializer(articulo)
                    #return Response({'error': False, 'msg': 'Artículo encontrado.', 'data': articulo_serializer.data}, status = status.HTTP_200_OK)
                    return Response(articulo_serializer.data, status = status.HTTP_200_OK)
                except Articulo.DoesNotExist:
                    return Response({'error': True, 'msg': 'El artículo no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_art=None, *args, **kwargs):
        try:
            try:
                articulo = Articulo.objects.get(id_art = id_art)
                articulo_serializer = self.get_serializer(articulo, data=request.data)
                if articulo_serializer.is_valid():
                    articulo_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': articulo_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': articulo_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Articulo.DoesNotExist:
                return Response({'error': True, 'msg': 'El artículo no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_art=None, *args, **kwargs):
        try:
            try:
                articulo = Articulo.objects.get(id_art = id_art)
                articulo.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Articulo.DoesNotExist:
                return Response({'error': True, 'msg': 'El artículo no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicArticuloApi(generics.ListAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        articulos = Articulo.objects.all()
        articulos_serializer = self.get_serializer(articulos, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(articulos_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': articulos_serializer.data}, status = status.HTTP_200_OK)
           
class PublicArticuloDetailApi(generics.RetrieveAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_art=None, *args, **kwars):
        try:
            try:
                articulo = Articulo.objects.get(id_art = id_art)
                articulo_serializer = self.get_serializer(articulo)
                return Response({'error': False, 'msg': 'Artículo encontrado.', 'data': articulo_serializer.data}, status = status.HTTP_200_OK)
            except Articulo.DoesNotExist:
                return Response({'error': True, 'msg': 'El artículo no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class LibroApi(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_LIBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_LIBRO.value)
        if view_perm or change_perm:
            libros = Libro.objects.all()
            libros_serializer = self.get_serializer(libros, many=True)
            msg = 'No se han encontrado registros.'
            if(libros_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': libros_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_LIBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_LIBRO.value)
        libro_serializer = self.get_serializer(data=request.data)
        if libro_serializer.is_valid():
            libro_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': libro_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': libro_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class LibroDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Libro, pk=self.kwargs.get('id_lib'))
        except:
            return None

    def get(self, request, id_lib=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_LIBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_LIBRO.value)
        if view_perm or change_perm:
            try:
                try:
                    libro = Libro.objects.get(id_lib = id_lib)
                    libro_serializer = self.get_serializer(libro)
                    #return Response({'error': False, 'msg': 'Libro encontrado.', 'data': libro_serializer.data}, status = status.HTTP_200_OK)
                    return Response(libro_serializer.data, status = status.HTTP_200_OK)
                except Libro.DoesNotExist:
                    return Response({'error': True, 'msg': 'El libro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_lib=None, *args, **kwargs):
        try:
            try:
                libro = Libro.objects.get(id_lib = id_lib)
                libro_serializer = self.get_serializer(libro, data=request.data)
                if libro_serializer.is_valid():
                    libro_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': libro_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': libro_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Libro.DoesNotExist:
                return Response({'error': True, 'msg': 'El libro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_lib=None, *args, **kwargs):
        try:
            try:
                libro = Libro.objects.get(id_lib = id_lib)
                libro.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Libro.DoesNotExist:
                return Response({'error': True, 'msg': 'El libro no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicLibroApi(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        libros = Libro.objects.all()
        libros_serializer = self.get_serializer(libros, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(libros_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': libros_serializer.data}, status = status.HTTP_200_OK)
           
class PublicLibroDetailApi(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_lib=None, *args, **kwars):
        try:
            try:
                libro = Libro.objects.get(id_lib = id_lib)
                libro_serializer = self.get_serializer(libro)
                return Response({'error': False, 'msg': 'Libro encontrado.', 'data': libro_serializer.data}, status = status.HTTP_200_OK)
            except Libro.DoesNotExist:
                return Response({'error': True, 'msg': 'El libro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class PIntelectualApi(generics.ListCreateAPIView):
    queryset = PIntelectual.objects.all()
    serializer_class = PIntelectualSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_PINTELECTUAL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PINTELECTUAL.value)
        if view_perm or change_perm:
            pintelectuales = PIntelectual.objects.all()
            pintelectuales_serializer = self.get_serializer(pintelectuales, many=True)
            msg = 'No se han encontrado registros.'
            if(pintelectuales_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': pintelectuales_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_PINTELECTUAL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PINTELECTUAL.value)
        pintelectual_serializer = self.get_serializer(data=request.data)
        if pintelectual_serializer.is_valid():
            pintelectual_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': pintelectual_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': pintelectual_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class PIntelectualDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = PIntelectual.objects.all()
    serializer_class = PIntelectualSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(PIntelectual, pk=self.kwargs.get('id_pin'))
        except:
            return None

    def get(self, request, id_pin=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_PINTELECTUAL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_PINTELECTUAL.value)
        if view_perm or change_perm:
            try:
                try:
                    pintelectual = PIntelectual.objects.get(id_pin = id_pin)
                    pintelectual_serializer = self.get_serializer(pintelectual)
                    #return Response({'error': False, 'msg': 'Propiedad intelectual encontrada.', 'data': pintelectual_serializer.data}, status = status.HTTP_200_OK)
                    return Response(pintelectual_serializer.data, status = status.HTTP_200_OK)
                except PIntelectual.DoesNotExist:
                    return Response({'error': True, 'msg': 'La Propiedad Intelectual no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_pin=None, *args, **kwargs):
        try:
            try:
                pintelectual = PIntelectual.objects.get(id_pin = id_pin)
                pintelectual_serializer = self.get_serializer(pintelectual, data=request.data)
                if pintelectual_serializer.is_valid():
                    pintelectual_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': pintelectual_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': pintelectual_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except PIntelectual.DoesNotExist:
                return Response({'error': True, 'msg': 'La Propiedad Intelectual no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_pin=None, *args, **kwargs):
        try:
            try:
                pintelectual = PIntelectual.objects.get(id_pin=id_pin)
                pintelectual.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except PIntelectual.DoesNotExist:
                return Response({'error': True, 'msg': 'La Propiedad Intelectual no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicPIntelectualApi(generics.ListAPIView):
    queryset = PIntelectual.objects.all()
    serializer_class = PIntelectualSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        pintelectuales = PIntelectual.objects.all()
        pintelectuales_serializer = self.get_serializer(pintelectuales, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(pintelectuales_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': pintelectuales_serializer.data}, status = status.HTTP_200_OK)
           
class PublicPIntelectualDetailApi(generics.RetrieveAPIView):
    queryset = PIntelectual.objects.all()
    serializer_class = PIntelectualSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_pin=None, *args, **kwars):
        try:
            try:
                pintelectual = PIntelectual.objects.get(id_pin = id_pin)
                pintelectual_serializer = self.get_serializer(pintelectual)
                return Response({'error': False, 'msg': 'Propiedad intelectual encontrada.', 'data': pintelectual_serializer.data}, status = status.HTTP_200_OK)
            except PIntelectual.DoesNotExist:
                return Response({'error': True, 'msg': 'La Propiedad Intelectual no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class TesisApi(generics.ListCreateAPIView):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_TESIS.value)
        change_perm = request.user.has_perm(permiso.CHANGE_TESIS.value)
        if view_perm or change_perm:
            tesis = Tesis.objects.all()
            tesis_serializer = self.get_serializer(tesis, many=True)
            msg = 'No se han encontrado registros.'
            if(tesis_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': tesis_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_TESIS.value)
        change_perm = request.user.has_perm(permiso.CHANGE_TESIS.value)
        tesis_serializer = self.get_serializer(data=request.data)
        if tesis_serializer.is_valid():
            tesis_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': tesis_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': tesis_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class TesisDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Tesis, pk=self.kwargs.get('id_tes'))
        except:
            return None

    def get(self, request, id_tes=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_TESIS.value)
        change_perm = request.user.has_perm(permiso.CHANGE_TESIS.value)
        if view_perm or change_perm:
            try:
                try:
                    tesis = Tesis.objects.get(id_tes = id_tes)
                    tesis_serializer = self.get_serializer(tesis)
                    #return Response({'error': False, 'msg': 'Tesis encontrada.', 'data': tesis_serializer.data}, status = status.HTTP_200_OK)
                    return Response(tesis_serializer.data, status = status.HTTP_200_OK)
                except Tesis.DoesNotExist:
                    return Response({'error': True, 'msg': 'La tesis no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_tes=None, *args, **kwargs):
        try:
            try:
                tesis = Tesis.objects.get(id_tes = id_tes)
                tesis_serializer = self.get_serializer(tesis, data=request.data)
                if tesis_serializer.is_valid():
                    tesis_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': tesis_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': tesis_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Tesis.DoesNotExist:
                return Response({'error': True, 'msg': 'La tesis no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_tes=None, *args, **kwargs):
        try:
            try:
                tesis = Tesis.objects.get(id_tes = id_tes)
                tesis.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Tesis.DoesNotExist:
                return Response({'error': True, 'msg': 'La tesis no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicTesisApi(generics.ListAPIView):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        tesis = Tesis.objects.all()
        tesis_serializer = self.get_serializer(tesis, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(tesis_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': tesis_serializer.data}, status = status.HTTP_200_OK)
           
class PublicTesisDetailApi(generics.RetrieveAPIView):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_tes=None, *args, **kwars):
        try:
            try:
                tesis = Tesis.objects.get(id_tes = id_tes)
                tesis_serializer = self.get_serializer(tesis)
                return Response({'error': False, 'msg': 'Tesis encontrada.', 'data': tesis_serializer.data}, status = status.HTTP_200_OK)
            except Tesis.DoesNotExist:
                return Response({'error': True, 'msg': 'La tesis no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class CongresoApi(generics.ListCreateAPIView):
    queryset = Congreso.objects.all()
    serializer_class = CongresoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_CONGRESO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CONGRESO.value)
        if view_perm or change_perm:
            congresos = Congreso.objects.all()
            congresos_serializer = self.get_serializer(congresos, many=True)
            msg = 'No se han encontrado registros.'
            if(congresos_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': congresos_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_CONGRESO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CONGRESO.value)
        congreso_serializer = self.get_serializer(data=request.data)
        if congreso_serializer.is_valid():
            congreso_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': congreso_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': congreso_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class CongresoDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Congreso.objects.all()
    serializer_class = CongresoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Congreso, pk=self.kwargs.get('id_con'))
        except:
            return None

    def get(self, request, id_con=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_CONGRESO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CONGRESO.value)
        if view_perm or change_perm:
            try:
                try:
                    congreso = Congreso.objects.get(id_con = id_con)
                    congreso_serializer = self.get_serializer(congreso)
                    #return Response({'error': False, 'msg': 'Congreso encontrado.', 'data': congreso_serializer.data}, status = status.HTTP_200_OK)
                    return Response(congreso_serializer.data, status = status.HTTP_200_OK)
                except Congreso.DoesNotExist:
                    return Response({'error': True, 'msg': 'El congreso no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_con=None, *args, **kwargs):
        try:
            try:
                congreso = Congreso.objects.get(id_con = id_con)
                congreso_serializer = self.get_serializer(congreso, data=request.data)
                if congreso_serializer.is_valid():
                    congreso_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': congreso_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': congreso_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Congreso.DoesNotExist:
                return Response({'error': True, 'msg': 'El congreso no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_con=None, *args, **kwargs):
        try:
            try:
                congreso = Congreso.objects.get(id_con = id_con)
                congreso.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Congreso.DoesNotExist:
                return Response({'error': True, 'msg': 'El congreso no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicCongresoApi(generics.ListAPIView):
    queryset = Congreso.objects.all()
    serializer_class = CongresoSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        congresos = Congreso.objects.all()
        congresos_serializer = self.get_serializer(congresos, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(congresos_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': congresos_serializer.data}, status = status.HTTP_200_OK)
           
class PublicCongresoDetailApi(generics.RetrieveAPIView):
    queryset = Congreso.objects.all()
    serializer_class = CongresoSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_con=None, *args, **kwars):
        try:
            try:
                congreso = Congreso.objects.get(id_con = id_con)
                congreso_serializer = self.get_serializer(congreso)
                return Response({'error': False, 'msg': 'Congreso encontrado.', 'data': congreso_serializer.data}, status = status.HTTP_200_OK)
            except Congreso.DoesNotExist:
                return Response({'error': True, 'msg': 'El congreso no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

#Miembros
class MiembroApi(generics.ListCreateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_MIEMBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_MIEMBRO.value)
        if view_perm or change_perm:
            miembros = Miembro.objects.all()
            miembros_serializer = self.get_serializer(miembros, many=True)
            msg = 'No se han encontrado registros.'
            if(miembros_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': miembros_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_MIEMBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_MIEMBRO.value)
        miembro_serializer = self.get_serializer(data=request.data)
        if miembro_serializer.is_valid():
            miembro_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': miembro_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': miembro_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class MiembroDetailApi(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Miembro, pk=self.kwargs.get('id_miem'))
        except:
            return None

    def get(self, request, id_miem=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_MIEMBRO.value)
        change_perm = request.user.has_perm(permiso.CHANGE_MIEMBRO.value)
        if view_perm or change_perm:
            try:
                try:
                    miembro = Miembro.objects.get(id_miem = id_miem)
                    miembro_serializer = self.get_serializer(miembro)
                    #return Response({'error': False, 'msg': 'Registro encontrado.', 'data': miembro_serializer.data}, status = status.HTTP_200_OK)
                    return Response(miembro_serializer.data, status = status.HTTP_200_OK)
                except Miembro.DoesNotExist:
                    return Response({'error': True, 'msg': 'El registro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_miem=None, *args, **kwargs):
        try:
            try:
                miembro = Miembro.objects.get(id_miem = id_miem)
                miembro_serializer = self.get_serializer(miembro, data=request.data)
                if miembro_serializer.is_valid():
                    miembro_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': miembro_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': miembro_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Miembro.DoesNotExist:
                return Response({'error': True, 'msg': 'El registro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_miem=None, *args, **kwargs):
        try:
            try:
                miembro = Miembro.objects.get(id_miem = id_miem)
                if(str(miembro.imagen_miem) != ''):
                    if os.path.isfile(miembro.imagen_miem.path):
                        os.remove(miembro.imagen_miem.path)
                if(str(miembro.hvida_miem) != ''):
                    if os.path.isfile(miembro.hvida_miem.path):
                        os.remove(miembro.hvida_miem.path)
                miembro.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Miembro.DoesNotExist:
                return Response({'error': True, 'msg': 'El registro no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class MiembroFilterApi(generics.ListAPIView):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    http_method_names = ['get', 'options']

    def get(self, request, tipo=0, *args, **kwargs):
        try:
            if int(tipo)>=0 and int(tipo)<(len(SELECT_MIEMBRO)):
                miembros = Miembro.objects.filter(tipo_miem = tipo)
                miembros_serializer = self.get_serializer(miembros, many=True)
                msg = 'Lo sentimos. No se han encontrado miembros de este tipo.'
                if(miembros_serializer.data):
                    msg = 'Datos obtenidos correctamente.'
                return Response({'error': False, 'msg': msg, 'data': miembros_serializer.data}, status = status.HTTP_200_OK)
            return Response({'error': True, 'msg': 'Parametro ?(tipo de miembros)=/'+tipo+'/ enviado no existe. Ayuda '+str(SELECT_MIEMBRO), 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'Parametro ?(tipo de miembros)=/'+tipo+'/ enviado es inválido. Ayuda '+str(SELECT_MIEMBRO), 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class PublicMiembroApi(generics.ListAPIView):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        miembros = Miembro.objects.all()
        miembros_serializer = self.get_serializer(miembros, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(miembros_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': miembros_serializer.data}, status = status.HTTP_200_OK)
           
class PublicMiembroDetailApi(generics.RetrieveAPIView):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_miem=None, *args, **kwars):
        try:
            try:
                miembro = Miembro.objects.get(id_miem = id_miem)
                miembro_serializer = self.get_serializer(miembro)
                return Response({'error': False, 'msg': 'Registro encontrado.', 'data': miembro_serializer.data}, status = status.HTTP_200_OK)
            except Miembro.DoesNotExist:
                return Response({'error': True, 'msg': 'El registro no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

#Carousel de imágenes
class CarouselApi(generics.ListCreateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_CAROUSEL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CAROUSEL.value)
        if view_perm or change_perm:
            carousels = Carousel.objects.all()
            carousels_serializer = self.get_serializer(carousels, many=True)
            msg = 'No se han encontrado registros.'
            if(carousels_serializer.data):
                msg = 'Datos obtenidos correctamente.'
            return Response({'error': False, 'msg': msg, 'data': carousels_serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para ver los registros.', 'data': None}, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        view_perm = request.user.has_perm(permiso.VIEW_CAROUSEL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CAROUSEL.value)
        carousel_serializer = self.get_serializer(data=request.data)
        if carousel_serializer.is_valid():
            carousel_serializer.save()
            if view_perm or change_perm:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': carousel_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': None}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': carousel_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class CarouselDetailApi(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Carousel, pk=self.kwargs.get('id_car'))
        except:
            return None

    def get(self, request, id_car=None, *args, **kwars):
        view_perm = request.user.has_perm(permiso.VIEW_CAROUSEL.value)
        change_perm = request.user.has_perm(permiso.CHANGE_CAROUSEL.value)
        if view_perm or change_perm:
            try:
                try:
                    carousel = Carousel.objects.get(id_car = id_car)
                    carousel_serializer = self.get_serializer(carousel)
                    #return Response({'error': False, 'msg': 'Carousel encontrado.', 'data': carousel_serializer.data}, status = status.HTTP_200_OK)
                    return Response(carousel_serializer.data, status = status.HTTP_200_OK)
                except Carousel.DoesNotExist:
                    return Response({'error': True, 'msg': 'El carousel no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': True, 'msg': 'Usted no tiene permiso para realizar esta acción.', 'data': None}, status = status.HTTP_403_FORBIDDEN)
    def put(self, request, id_car=None, *args, **kwargs):
        try:
            try:
                carousel = Carousel.objects.get(id_car = id_car)
                carousel_serializer = self.get_serializer(carousel, data=request.data)
                if carousel_serializer.is_valid():
                    carousel_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': carousel_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': carousel_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Carousel.DoesNotExist:
                return Response({'error': True, 'msg': 'El carousel no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_car=None, *args, **kwargs):
        try:
            try:
                carousel = Carousel.objects.get(id_car = id_car)
                if(str(carousel.imagen_car) != ''):
                    if os.path.isfile(carousel.imagen_car.path):
                        os.remove(carousel.imagen_car.path)
                carousel.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Carousel.DoesNotExist:
                return Response({'error': True, 'msg': 'El carousel no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class PublicCarouselApi(generics.ListAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        carousels = Carousel.objects.all()
        carousels_serializer = self.get_serializer(carousels, many=True)
        msg = 'Lo sentimos. No se han encontrado registros.'
        if(carousels_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': carousels_serializer.data}, status = status.HTTP_200_OK)
           
class PublicCarouselDetailApi(generics.RetrieveAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    http_method_names = ['get', 'options']

    def get(self, request, id_car=None, *args, **kwars):
        try:
            try:
                carousel = Carousel.objects.get(id_car = id_car)
                carousel_serializer = self.get_serializer(carousel)
                return Response({'error': False, 'msg': 'Ítem del carousel de imágenes encontrado.', 'data': carousel_serializer.data}, status = status.HTTP_200_OK)
            except Carousel.DoesNotExist:
                return Response({'error': True, 'msg': 'El ítem del carousel de imágenes no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

#Tema por usuario
class TemaApi(generics.ListCreateAPIView):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        temas = Tema.objects.all()
        temas_serializer = self.get_serializer(temas, many=True)
        msg = 'No se han encontrado registros.'
        if(temas_serializer.data):
            msg = 'Datos obtenidos correctamente.'
        return Response({'msg': msg, 'data': temas_serializer.data}, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        tema_serializer = self.get_serializer(data=request.data)
        if tema_serializer.is_valid():
            tema_serializer.save()
            return Response({'error': False,'msg': 'Registro Exitoso!!', 'data': tema_serializer.data}, status = status.HTTP_201_CREATED)
        return Response({'error': True, 'msg': tema_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class TemaDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_object(self):
        try:
            return get_object_or_404(Tema, pk=self.kwargs.get('id_tem'))
        except:
            return None

    def get(self, request, id_tem=None, *args, **kwars):
        try:
            try:
                tema = Tema.objects.get(id_tem = id_tem)
                tema_serializer = self.get_serializer(tema)
                #return Response({'error': False, 'msg': 'Tema encontrado.', 'data': tema_serializer.data}, status = status.HTTP_200_OK)
                return Response(tema_serializer.data, status = status.HTTP_200_OK)
            except Tema.DoesNotExist:
                return Response({'error': True, 'msg': 'El tema no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def put(self, request, id_tem=None, *args, **kwargs):
        try:
            try:
                tema = Tema.objects.get(id_tem = id_tem)
                tema_serializer = self.get_serializer(tema, data=request.data)
                if tema_serializer.is_valid():
                    tema_serializer.save()
                    return Response({'error': False,'msg': 'Actualización Exitosa!!', 'data': tema_serializer.data}, status = status.HTTP_200_OK)
                return Response({'error': True, 'msg': tema_serializer.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
            except Tema.DoesNotExist:
                return Response({'error': True, 'msg': 'El tema no existe.', 'data': None}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_tem=None, *args, **kwargs):
        try:
            try:
                tema = Tema.objects.get(id_tem = id_tem)
                tema.delete()
                return Response({'error': False, 'msg': 'Registro Eliminado Exitosamente!!'}, status = status.HTTP_200_OK)
            except Tema.DoesNotExist:
                return Response({'error': True, 'msg': 'El tema no existe.'}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.'}, status = status.HTTP_400_BAD_REQUEST)

class TemaByUserApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TemaSerializer
    http_method_names = ['get', 'options']

    def get(self, request, fk_id_usu=None, *args, **kwargs):
        try:
            tema = Tema.objects.filter(fk_id_usu = fk_id_usu).first()
            tema_serializer = self.get_serializer(tema)
            msg = 'El usuario ahún no ha registrado un tema.'
            if(tema_serializer.data):
                msg = 'Tema encontrado.'
            return Response({'error': False, 'msg': msg, 'data': tema_serializer.data}, status = status.HTTP_200_OK)
        except:
            return Response({'error': True, 'msg': 'El id enviado es un UUID inválido.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)