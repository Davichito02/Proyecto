from django import forms
from users.models import Usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion'
        )