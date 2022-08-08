import uuid
from users.models import *
from django.db import models
from myproject.selects import *
from myproject.validators import *

# Create your models here.
#Investigación
class Proyecto(models.Model):
    id_pro = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_pro = models.CharField(max_length=100, verbose_name='Título')
    fecha_pro = models.DateField(verbose_name="Fecha")
    responsable_pro = models.CharField(max_length=100, verbose_name='Responsable')
    investigadores_pro = models.CharField(max_length=500, verbose_name='Investigadores')
    periodo_pro = models.CharField(max_length=50, verbose_name='Periodo')
    descripcion_pro = models.CharField(max_length=500, verbose_name='Descripción')

    def __str__(self):
        return self.titulo_pro
    class Meta:
        verbose_name= 'Proyecto'
        verbose_name_plural= 'Proyectos'
        db_table= 'proyecto'
        ordering=['id_pro']

class Archivo(models.Model):
    id_arch = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    archivo_arch = models.FileField(
        upload_to='Archivos/Proyectos/%Y/%m', max_length=300, verbose_name='Archivo', 
        null=False, blank=True, default='',  validators=[validate_file_extension],
        help_text=('Solo archivos PDF. Inválido el envío de múltiples archivos,'+
        ' si selecciona más de uno, se subirá el útlimo archivo enviado.')
    )
    fk_id_pro= models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='Proyecto')

    def __str__(self):
        return self.id_arch
    class Meta:
        verbose_name= 'Archivo'
        verbose_name_plural= 'Archivos'
        db_table= 'archivo'
        ordering=['id_arch']

#Publicaciones
class Articulo(models.Model):
    id_art = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_art = models.CharField(max_length=100, verbose_name='Título')
    enlace_art = models.CharField(max_length=300, verbose_name='Enlace')
    indexacion_art = models.CharField(max_length=100, verbose_name='Indexación')
    desc_art = models.CharField(max_length=100, verbose_name='Desconocido')
    autores_art = models.CharField(max_length=500, verbose_name='Autores')
    issn_art = models.CharField(max_length=100, verbose_name='ISSN')

    def __str__(self):
        return self.titulo_art
    class Meta:
        verbose_name= 'Artículo'
        verbose_name_plural= 'Artículos'
        db_table= 'articulo'
        ordering=['id_art']

class Libro(models.Model):
    id_lib = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_lib = models.CharField(max_length=100, verbose_name='Título')
    desc_lib = models.CharField(max_length=100, verbose_name='Desconocido')
    autores_lib = models.CharField(max_length=500, verbose_name='Autores')
    issn_lib = models.CharField(max_length=100, verbose_name='ISSN')
    tipo_lib = models.IntegerField(
        null=False, blank=True, 
        verbose_name='Tipo',
        choices=SELECT_LIBRO, default=0
    )

    def __str__(self):
        return self.titulo_lib
    class Meta:
        verbose_name= 'Libro'
        verbose_name_plural= 'Libros'
        db_table= 'libro'
        ordering=['id_lib']

class PIntelectual(models.Model): #Propiedad Intelectual
    id_pin = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_pin = models.CharField(max_length=100, verbose_name='Título')
    fecha_pin = models.DateField(verbose_name="Fecha")

    def __str__(self):
        return self.titulo_pin
    class Meta:
        verbose_name= 'P. Intelecutal'
        verbose_name_plural= 'P. Intelectuales'
        db_table= 'p_intelectual'
        ordering=['id_pin']

class Tesis(models.Model):
    id_tes = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_tes = models.CharField(max_length=100, verbose_name='Título')
    anio_tes = models.CharField(max_length=4, verbose_name='Año')
    directores_tes = models.CharField(max_length=500, verbose_name='Directores')
    autores_tes = models.CharField(max_length=500, verbose_name='Autores')
    universidad_tes = models.CharField(max_length=200, verbose_name='Universidad')
    tipo_tes = models.IntegerField(
        null=False, blank=True, 
        verbose_name='Tipo',
        choices=SELECT_TESIS, default=0
    )

    def __str__(self):
        return self.titulo_tes
    class Meta:
        verbose_name= 'Tesis'
        verbose_name_plural= 'Tesis'
        db_table= 'tesis'
        ordering=['id_tes']

class Congreso(models.Model):
    id_con = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_con = models.CharField(max_length=100, verbose_name='Título')
    autor_con = models.CharField(max_length=100, verbose_name='Autor')
    anio_con = models.CharField(max_length=4, verbose_name='Año')
    numero_con = models.CharField(max_length=5, verbose_name='Número de congreso')

    def __str__(self):
        return self.titulo_con
    class Meta:
        verbose_name= 'Congreso'
        verbose_name_plural= 'Congresos'
        db_table= 'congreso'
        ordering=['id_con']

#Miembros
class Miembro(models.Model):
    id_miem = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    nombre_miem = models.CharField(max_length=100, verbose_name='Nombres')
    apellido_miem = models.CharField(max_length=100, verbose_name='Apellidos')
    correo_miem = models.CharField(max_length=100, verbose_name='Correo', unique=True)
    telefono_miem = models.CharField(max_length=10, verbose_name='Teléfono')
    imagen_miem = models.ImageField(
        upload_to='Imagenes/Miembros/%Y/%m', max_length=300, verbose_name='Foto', 
        null=False, blank=True, default='',
        help_text=('Solo Imágenes. Inválido el envío de múltiples imágenes,'+
        ' si selecciona más de una, se subirá la útlima imágen enviada.')
    )
    cargo_miem = models.CharField(max_length=100, verbose_name='Cargo')
    descripcion_miem = models.CharField(max_length=500, verbose_name='Descripción')
    hvida_miem = models.FileField(
        upload_to='Archivos/Miembros/%Y/%m', max_length=300, verbose_name='Hoja de vida', 
        null=False, blank=True, default='', validators=[validate_file_extension],
        help_text=('Solo archivos PDF. Inválido el envío de múltiples archivos,'+
        ' si selecciona más de uno, se subirá el útlimo archivo enviado.')
    )
    tipo_miem = models.IntegerField(
        null=False, blank=True, 
        verbose_name='Tipo',
        choices=SELECT_MIEMBRO, default=0
    )

    def __str__(self):
        return self.nombre_miem + " " + self.apellido_miem
    class Meta:
        verbose_name= 'Miembro'
        verbose_name_plural= 'Miembros'
        db_table= 'miembro'
        ordering=['id_miem']

#Tema por usuario
class Tema(models.Model):
    id_tem = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    nombre_tem = models.CharField(max_length=100,verbose_name='Tema')
    posicion_tem = models.CharField(max_length=10,verbose_name='Posición')
    fk_id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.nombre_tem
    class Meta:
        verbose_name= 'Tema'
        verbose_name_plural= 'Temas'
        db_table= 'tema'
        ordering=['id_tem']

#Carousel de imágenes
class Carousel(models.Model):
    id_car = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulopr_car = models.CharField(max_length=50, verbose_name='Título principal')
    titulosec_car = models.CharField(max_length=50, verbose_name='Título secundario')
    subtitulo_car = models.CharField(max_length=100, verbose_name='Subtítulo')
    imagen_car = models.ImageField(
        upload_to='Imagenes/Carousel/%Y/%m', max_length=300, verbose_name='Imágen', 
        null=False, blank=True, default='',
        help_text=('Solo Imágenes. Inválido el envío de múltiples imágenes,'+
        ' si selecciona más de una, se subirá la útlima imágen enviada.')
    )

    def __str__(self):
        return self.titulopr_car + " " + self.titulosec_car
    class Meta:
        verbose_name= 'Carousel'
        verbose_name_plural= 'Carousels'    
        db_table= 'carousel'
        ordering=['id_car']