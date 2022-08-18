import uuid
from users.models import *
from django.db import models
from myproject.choices import *
from myproject.validators import *

custom_email_validator= CustomEmailValidator()
phone_number_validator= PhoneNumberValidator()
issn_number_validator= ISSNNumberValidator()
number_validator= NumberValidator()

# Create your models here.
#Miembros
class Miembro(models.Model):
    id_miem = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    nombre_miem = models.CharField(max_length=100, verbose_name='Nombres')
    apellido_miem = models.CharField(max_length=100, verbose_name='Apellidos')
    correo_miem = models.CharField(
        max_length=150, verbose_name='Correo electrónico',
        help_text=('Requerido.'),
        unique=True, validators=[custom_email_validator],
        error_messages={
            'unique': ("Ya existe un miembro con esta dirección de correo electrónico."),
        },
    )
    telefono_miem = models.CharField(
        max_length=10, verbose_name='Teléfono',
        help_text=('Requerido. Formato: xxxxxxxxxx.'), validators=[phone_number_validator]
    )
    imagen_miem = models.ImageField(
        upload_to='Imagenes/Miembros/%Y/%m', max_length=300, verbose_name='Foto', 
        null=False, blank=True, default='',
        help_text=(
            'Solo Imágenes. Inválido el envío de múltiples imágenes, '
            'si selecciona más de una, se subirá la útlima imágen enviada.'
        )
    )
    cargo_miem = models.CharField(max_length=100, verbose_name='Cargo')
    descripcion_miem = models.CharField(max_length=500, verbose_name='Descripción')
    hvida_miem = models.FileField(
        upload_to='Archivos/Miembros/%Y/%m', max_length=300, verbose_name='Hoja de vida', 
        null=False, blank=True, default='', validators=[validate_file_extension],
        help_text=(
            'Solo archivos PDF. Inválido el envío de múltiples archivos, '
            'si selecciona más de uno, se subirá el útlimo archivo enviado.'
        )
    )
    tipo_miem = models.IntegerField(
        null=False, blank=False, verbose_name='Tipo',
        choices=CHOICE_MIEMBRO, default=0
    )

    def __str__(self):
        return " "+ self.nombre_miem + " " + self.apellido_miem
    class Meta:
        verbose_name= 'Miembro'
        verbose_name_plural= 'Miembros'
        db_table= 'miembro'
        ordering=['id_miem']

#Investigación
class Proyecto(models.Model):
    id_pro = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_pro = models.CharField(max_length=200, verbose_name='Título',)
    fecha_pro = models.DateField(
        verbose_name="Fecha", validators=[validate_fecha],
        help_text=(
            'Ingrese solo fechas mayores al año 2000 y menores al año actual.'
        )
    )
    responsables_pro = models.ManyToManyField(Miembro, related_name='proyectos', verbose_name='Responsables')
    investigadores_pro = models.CharField(max_length=500, verbose_name='Investigadores')
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
        help_text=(
            'Solo archivos PDF. Inválido el envío de múltiples archivos, '
            'si selecciona más de uno, se subirá el útlimo archivo enviado.'
        )
    )
    fk_id_pro= models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='Proyecto')

    def __str__(self):
        return str(self.id_arch)
    class Meta:
        verbose_name= 'Archivo'
        verbose_name_plural= 'Archivos'
        db_table= 'archivo'
        ordering=['id_arch']

#Publicaciones
class Articulo(models.Model):
    id_art = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_art = models.CharField(max_length=200, verbose_name='Título')
    enlace_art = models.URLField(max_length=500, verbose_name='Enlace')
    indexacion_art = models.CharField(max_length=100, verbose_name='Indexación')
    autores_art = models.ManyToManyField(Miembro, related_name='articulos', verbose_name='Autores')
    issn_art = models.CharField(
        max_length=9, verbose_name='ISSN', validators=[issn_number_validator],
        help_text='Requerido. Formato: xxxx-xxxx'
    )

    def __str__(self):
        return self.titulo_art
    class Meta:
        verbose_name= 'Artículo'
        verbose_name_plural= 'Artículos'
        db_table= 'articulo'
        ordering=['id_art']

class Libro(models.Model):
    id_lib = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_lib = models.CharField(max_length=200, verbose_name='Título')
    autores_lib = models.ManyToManyField(Miembro, related_name='libros', verbose_name='Autores')
    issn_lib = models.CharField(
        max_length=9, verbose_name='ISSN', validators=[issn_number_validator],
        help_text='Requerido. Formato: xxxx-xxxx'
    )
    tipo_lib = models.IntegerField(
        null=False, blank=False, 
        verbose_name='Tipo',
        choices=CHOICE_LIBRO, default=0
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
    titulo_pin = models.CharField(max_length=200, verbose_name='Título')
    fecha_pin = models.DateField(
        verbose_name="Fecha", validators=[validate_fecha],
        help_text=(
            'Ingrese solo fechas mayores al año 2000 y menores al año actual.'
        )
    )

    def __str__(self):
        return self.titulo_pin
    class Meta:
        verbose_name= 'P. Intelecutal'
        verbose_name_plural= 'P. Intelectuales'
        db_table= 'p_intelectual'
        ordering=['id_pin']

class Tesis(models.Model):
    id_tes = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulo_tes = models.CharField(max_length=200, verbose_name='Título')
    anio_tes = models.CharField(
        max_length=4, verbose_name='Año', validators=[validate_anio],
        help_text=(
            'Ingrese solo años mayores a 2000 y menores al año actual.'
        )
    )
    directores_tes = models.CharField(max_length=500, verbose_name='Directores')
    autores_tes = models.ManyToManyField(Miembro, related_name='tesis', verbose_name='Autores')
    universidad_tes = models.CharField(max_length=200, verbose_name='Universidad')
    tipo_tes = models.IntegerField(
        null=False, blank=False, 
        verbose_name='Tipo',
        choices=CHOICE_TESIS, default=0
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
    titulo_con = models.CharField(max_length=200, verbose_name='Título')
    autores_con = models.ManyToManyField(Miembro, related_name='congresos', verbose_name='Autores')
    anio_con = models.CharField(
        max_length=4, verbose_name='Año', validators=[validate_anio],
        help_text=(
            'Ingrese solo años mayores a 2000 y menores al año actual.'
        )
    )
    numero_con = models.CharField(
        max_length=10, verbose_name='Número de congreso', validators=[number_validator],
        help_text=('Requerido. Ingrese solo numeros.')
    )

    def __str__(self):
        return self.titulo_con
    class Meta:
        verbose_name= 'Congreso'
        verbose_name_plural= 'Congresos'
        db_table= 'congreso'
        ordering=['id_con']
        
#Capacitaciones
class Capacitacion(models.Model):
    id_cap = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    imagen_cap = models.ImageField(
        upload_to='Imagenes/Capacitacion/%Y/%m', max_length=300, verbose_name='Imágen', 
        null=False, blank=True, default='',
        help_text=(
            'Solo Imágenes. Inválido el envío de múltiples imágenes, '
            'si selecciona más de una, se subirá la útlima imágen enviada.'
        )
    )
    descripcion_cap = models.CharField(max_length=500, verbose_name='Descripción')
    fecha_cap = models.DateField(
        verbose_name="Fecha", validators=[validate_fecha],
        help_text=(
            'Ingrese solo fechas mayores al año 2000 y menores al año actual.'
        )
    )
    tipo_cap = models.IntegerField(
        null=False, blank=False, 
        verbose_name='Tipo',
        choices=CHOICE_CAPACITACION, default=0
    )

    def __str__(self):
        return str(self.id_cap)
    class Meta:
        verbose_name= 'Capacitación'
        verbose_name_plural= 'Capacitaciones'
        db_table= 'capacitacion'
        ordering=['id_cap']

#Carousel de imágenes
class Carousel(models.Model):
    id_car = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    titulopr_car = models.CharField(max_length=50, verbose_name='Título principal')
    titulosec_car = models.CharField(max_length=50, verbose_name='Título secundario')
    subtitulo_car = models.CharField(max_length=200, verbose_name='Subtítulo')
    imagen_car = models.ImageField(
        upload_to='Imagenes/Carousel/%Y/%m', max_length=300, verbose_name='Imágen', 
        null=False, blank=True, default='',
        help_text=(
            'Solo Imágenes. Inválido el envío de múltiples imágenes, '
            'si selecciona más de una, se subirá la útlima imágen enviada.'
        )
    )

    def __str__(self):
        return self.titulopr_car + " " + self.titulosec_car
    class Meta:
        verbose_name= 'Carousel'
        verbose_name_plural= 'Carousels'    
        db_table= 'carousel'
        ordering=['id_car']

#Tema por usuario
class Tema(models.Model):
    id_tem = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='Código')
    nombre_tem = models.CharField(max_length=100,verbose_name='Tema')
    fk_id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.nombre_tem
    class Meta:
        verbose_name= 'Tema'
        verbose_name_plural= 'Temas'
        db_table= 'tema'
        ordering=['id_tem']
