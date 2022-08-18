import os, re, datetime
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core import validators

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    #valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Extensión de archivo no admitida.')

def validate_anio(value):
    regex= r'^(2[\d]{3})+\Z'
    validator= re.compile(regex)
    if validator.search(value):
        current_date = datetime.date.today()
        current_year = current_date.strftime("%Y")
        if int(value)> int(current_year):
            raise ValidationError(u'El año ingresado es mayor al año actual.')
    else:
        raise ValidationError(
            u'Formato de año inválido. Este valor puede contener solo números '
            'ejemplo 2018, mínimo y máximo 4 números, mayores a 2000 y menores al año actual.'
        )

def validate_fecha(value):
    current_date = datetime.date.today()
    min_date = datetime.date(2000, 1, 1)
    if value> current_date:
        raise ValidationError(u'La fecha ingresada es mayor a la fecha actual.')
    elif value< min_date:
        raise ValidationError(u'La fecha ingresada es menor al año 2000.')

@deconstructible
class CustomEmailValidator(validators.RegexValidator):
    regex = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))+\Z'
    message = (
        'Ingrese un correo electrónico valido.'
    )
    flags = 0
    
@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^([\d]{10})+\Z'
    message = (
        'Ingrese un número de teléfono valido. Este valor puede contener solo números, '
        'ejemplo 0999999999, formato: xxxxxxxxxx'
    )
    flags = 0

@deconstructible
class ISSNNumberValidator(validators.RegexValidator):
    regex = r'^([0-9]{4}-[0-9]{3}[0-9xX])+\Z'
    message = (
        'Ingrese un ISSN valido. Este valor puede contener solo números o tambien al final una X, '
        'ejemplo 1234-5678, formato: xxxx-xxxx'
    )
    flags = 0

@deconstructible
class NumberValidator(validators.RegexValidator):
    regex = r'^[\d]+\Z'
    message = (
        'Ingrese un número valido. Este valor puede contener solo números.'
    )
    flags = 0
