from .models import *
from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'content_type_id',
            'codename'
        )

class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'is_superuser',
            'is_active',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
            'user_permissions',
        )
        read_only_fields = ('user_permissions',)
        extra_kwargs = {'password': {'write_only': True}}

class UsuarioAdminSerializerPerfil(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_superuser',
            'is_active',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
            'user_permissions',
        )
        read_only_fields = ('username', 'email')

class UsuarioAdminSerializerCredentials(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'is_superuser',
            'is_active',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
            'user_permissions',
        )
        read_only_fields = (
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'avatar',
            'work',
            'direccion',
            'telefono',
            'empresa',
            'descripcion',
            'user_permissions',
        )
        extra_kwargs = {'password': {'write_only': True}}
