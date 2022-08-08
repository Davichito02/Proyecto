from users.models import *
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
        )
        extra_kwargs = {'password': {'write_only': True}}
        

class UsuarioSerializerPerfil(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
        )
        read_only_fields = ('username', 'email')
       

class UsuarioSerializerCredentials(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
        )
        read_only_fields = (
            'first_name', 
            'last_name',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
        )
        extra_kwargs = {'password': {'write_only': True}}
