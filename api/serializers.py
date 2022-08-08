from rest_framework import serializers
from .models import *

# Create your serializers here.
#Investigación
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = (
            'id_pro',
            'titulo_pro',
            'fecha_pro',
            'responsable_pro',
            'investigadores_pro',
            'periodo_pro',
            'descripcion_pro',
        )

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
            'desc_art',
            'autores_art',    
            'issn_art',
        )

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = (
            'id_lib',
            'titulo_lib',
            'desc_lib',
            'autores_lib',
            'issn_lib',
            'tipo_lib',
        )

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

class CongresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congreso
        fields = (
            'id_con',
            'titulo_con',
            'autor_con',
            'anio_con',
            'numero_con',
        )

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
        )

#Tema por usuario
class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ('id_tem','nombre_tem','posicion_tem','fk_id_usu')

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