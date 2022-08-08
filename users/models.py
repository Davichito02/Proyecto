from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class Usuario(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'), 
        unique=True, max_length=100
    )
    #USERNAME_FIELD = 'email' 
    #REQUIRED_FIELDS = ['username']
    avatar =models.ImageField(
        upload_to='Imagenes/User/%Y/%m', max_length=300, verbose_name='Imágen', 
        null=False, blank=True, default='',
        help_text=('Solo Imágenes. Inválido el envío de múltiples imágenes,'+
        ' si selecciona más de una, se subirá la útlima imágen enviada.')
    )
    work = models.CharField(verbose_name='Trabajo',max_length=100)
    direccion = models.CharField(verbose_name='Dirección',max_length=150)
    telefono = models.CharField(verbose_name='Teléfono',max_length=10)
    empresa = models.CharField(verbose_name='Empresa',max_length=150)
    descripcion = models.CharField(verbose_name='Descripción',max_length=300)

    class Meta:
        verbose_name= 'Usuario'
        verbose_name_plural= 'Usuarios'
        db_table= 'usuario'
        ordering=['id']