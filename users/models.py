from django.db import models
from myproject.validators import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin

custom_email_validator= CustomEmailValidator()
phone_number_validator= PhoneNumberValidator()

class Usuario(AbstractUser, PermissionsMixin):
    email = models.CharField(
        _('email address'), max_length=150, help_text=('Requerido.'), 
        unique=True, validators=[custom_email_validator],
        error_messages={
            'unique': ("Ya existe un usuario con esta dirección de correo electrónico."),
        },
    )
    #USERNAME_FIELD = 'email' 
    #REQUIRED_FIELDS = ['username']
    avatar =models.ImageField(
        upload_to='Imagenes/User/%Y/%m', max_length=300, verbose_name='Imágen', 
        null=False, blank=True, default='',
        help_text=(
            'Solo Imágenes. Inválido el envío de múltiples imágenes, '
            'si selecciona más de una, se subirá la útlima imágen enviada.'
        )
    )
    work = models.CharField(verbose_name='Trabajo',max_length=100)
    direccion = models.CharField(verbose_name='Dirección',max_length=150)
    telefono = models.CharField(
        max_length=10, verbose_name='Teléfono',
        help_text=('Requerido. Formato: xxxxxxxxxx.'), validators=[phone_number_validator]
    )
    empresa = models.CharField(verbose_name='Empresa',max_length=150)
    descripcion = models.CharField(verbose_name='Descripción',max_length=300)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name= 'Usuario'
        verbose_name_plural= 'Usuarios'
        db_table= 'usuario'
        ordering=['id']