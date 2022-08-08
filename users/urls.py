from .views import *
from django.urls import path

urlpatterns = [
    path('permisos/', PermissionsApi.as_view(), name='all_permisos'),
    path('admin/', UsuarioAdminApi.as_view(), name='users_admin'),
    path('admin/<id>/', UsuarioAdminDetailApi.as_view(), name='users_admin_detail'),
    path('admin/credentials/<id>/', UsuarioAdminCredentialsApi.as_view(), name='users_admin_credentials'),
]
