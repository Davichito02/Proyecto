from rest_framework import serializers
from .models import *

# Create your serializers here.
#Miembros
class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = (
            'id_miem',
            'nombre_miem',
            'apellido_miem',
            'correo_miem',
            'telefono_miem',
            'imagen_miem',
            'cargo_miem',
            'descripcion_miem',
            'hvida_miem',
            'tipo_miem',

            'proyectos',
            'articulos',
            'libros',
            'tesis',
            'congresos',
        )

#Miembros
class PublicMiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = (
            'id_miem',
            'nombre_miem',
            'apellido_miem',
            'correo_miem',
            'telefono_miem',
            'imagen_miem',
            'cargo_miem',
            'descripcion_miem',
            'hvida_miem',
            'tipo_miem',

            'proyectos',
            'articulos',
            'libros',
            'tesis',
            'congresos',
        )
        depth = 1

#Investigación
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = (
            'id_pro',
            'titulo_pro',
            'fecha_pro',
            'responsables_pro',
            'investigadores_pro',
            'descripcion_pro',
        )

class ListProyectoSerializer(ProyectoSerializer):
    responsables_pro = serializers.StringRelatedField(many=True)

class PublicProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = (
            'id_pro',
            'titulo_pro',
            'fecha_pro',
            'responsables_pro',
            'investigadores_pro',
            'descripcion_pro',
        )
        depth = 1

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = ('id_arch', 'archivo_arch', 'fk_id_pro')

#Publicaciones
class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = (
            'id_art',
            'titulo_art',
            'enlace_art',
            'indexacion_art',
            'autores_art',    
            'issn_art',
        )

class ListArticuloSerializer(ArticuloSerializer):
    autores_art = serializers.StringRelatedField(many=True)

class PublicArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = (
            'id_art',
            'titulo_art',
            'enlace_art',
            'indexacion_art',
            'autores_art',    
            'issn_art',
        )
        depth = 1

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = (
            'id_lib',
            'titulo_lib',
            'autores_lib',
            'issn_lib',
            'tipo_lib',
        )

class ListLibroSerializer(LibroSerializer):
    autores_lib = serializers.StringRelatedField(many=True)

class PublicLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = (
            'id_lib',
            'titulo_lib',
            'autores_lib',
            'issn_lib',
            'tipo_lib',
        )
        depth = 1

class PIntelectualSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIntelectual
        fields = ('id_pin', 'titulo_pin', 'fecha_pin')

class TesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = (
            'id_tes',
            'titulo_tes',
            'anio_tes',
            'directores_tes',
            'autores_tes',
            'universidad_tes',
            'tipo_tes',
        )

class ListTesisSerializer(TesisSerializer):
    autores_tes = serializers.StringRelatedField(many=True)

class PublicTesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = (
            'id_tes',
            'titulo_tes',
            'anio_tes',
            'directores_tes',
            'autores_tes',
            'universidad_tes',
            'tipo_tes',
        )
        depth = 1

class CongresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congreso
        fields = (
            'id_con',
            'titulo_con',
            'autores_con',
            'anio_con',
            'numero_con',
        )

class ListCongresoSerializer(CongresoSerializer):
    autores_con = serializers.StringRelatedField(many=True)

class PublicCongresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congreso
        fields = (
            'id_con',
            'titulo_con',
            'autores_con',
            'anio_con',
            'numero_con',
        )
        depth = 1

#Capacitaciones
class CapacitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacitacion
        fields = (
            'id_cap',
            'imagen_cap',
            'descripcion_cap',
            'fecha_cap',
            'tipo_cap',
        )

#Carousel de imágenes
class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = (
            'id_car',
            'titulopr_car',
            'titulosec_car',
            'subtitulo_car',
            'imagen_car',
        )

#Tema por usuario
class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ('id_tem','nombre_tem','fk_id_usu')