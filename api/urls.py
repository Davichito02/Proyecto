from api.views import *
from django.urls import path

# Create your urls here.
urlpatterns = [
  #Investigación
  path('proyecto/', ProyectoApi.as_view(), name='private_proyecto'),
  path('proyecto/<id_pro>/', ProyectoDetailApi.as_view(), name='private_proyecto_detail'),
  path('public/proyecto/', PublicProyectoApi.as_view(), name='public_proyecto'),
  path('public/proyecto/<id_pro>/', PublicProyectoDetailApi.as_view(), name='public_proyecto_detail'),

  #Archivos por proyecto
  path('archivo/', ArchivoApi.as_view(), name='private_archivo'),
  path('archivo/<id_arch>/', ArchivoDetailApi.as_view(), name='private_archivo_detail'),
  path('archivo-by-proyecto/<fk_id_pro>/', ArchivoByProApi.as_view(), name='private_archivo_by_proyecto'),

  #Publicaciones
  path('articulo/', ArticuloApi.as_view(), name='private_articulo'),
  path('articulo/<id_art>/', ArticuloDetailApi.as_view(), name='private_articulo_detail'),
  path('public/articulo/', PublicArticuloApi.as_view(), name='public_articulo'),
  path('public/articulo/<id_art>/', PublicArticuloDetailApi.as_view(), name='public_articulo_detail'),

  path('libro/', LibroApi.as_view(), name='private_libro'),
  path('libro/<id_lib>/', LibroDetailApi.as_view(), name='private_libro_detail'),
  path('public/libro/', PublicLibroApi.as_view(), name='public_libro'),
  path('public/libro/<id_lib>/', PublicLibroDetailApi.as_view(), name='public_libro_detail'),

  path('pintelectual/', PIntelectualApi.as_view(), name='private_pintelectual'),
  path('pintelectual/<id_pin>/', PIntelectualDetailApi.as_view(), name='private_pintelectual_detail'),
  path('public/pintelectual/', PublicPIntelectualApi.as_view(), name='public_pintelectual'),
  path('public/pintelectual/<id_pin>/', PublicPIntelectualDetailApi.as_view(), name='public_pintelectual_detail'),

  path('tesis/', TesisApi.as_view(), name='private_tesis'),
  path('tesis/<id_tes>/', TesisDetailApi.as_view(), name='private_tesis_detail'),
  path('public/tesis/', PublicTesisApi.as_view(), name='public_tesis'),
  path('public/tesis/<id_tes>/', PublicTesisDetailApi.as_view(), name='public_tesis_detail'),

  path('congreso/', CongresoApi.as_view(), name='private_congreso'),
  path('congreso/<id_con>/', CongresoDetailApi.as_view(), name='private_congreso_detail'),
  path('public/congreso/', PublicCongresoApi.as_view(), name='public_congreso'),
  path('public/congreso/<id_con>/', PublicCongresoDetailApi.as_view(), name='public_congreso_detail'),

  #Miembros
  path('miembro/', MiembroApi.as_view(), name='private_miembro'),
  path('miembro/<id_miem>/', MiembroDetailApi.as_view(), name='private_miembro_detail'),
  path('public/miembro-with-filter/<tipo>/', MiembroFilterApi.as_view(), name='public_miembro_filter'),
  path('public/miembro/', PublicMiembroApi.as_view(), name='public_miembro'),
  path('public/miembro/<id_miem>/', PublicMiembroDetailApi.as_view(), name='public_miembro_detail'),

  #Tema por usuario
  path('tema/', TemaApi.as_view(), name='private_tema'),
  path('tema/<id_tem>/', TemaDetailApi.as_view(), name='private_tema_detail'),
  path('tema-by-user/<fk_id_usu>/', TemaByUserApi.as_view(), name='private_tema_by_user'),

  #Carousel de imágenes
  path('carousel/', CarouselApi.as_view(), name='private_carousel'),
  path('carousel/<id_car>/', CarouselDetailApi.as_view(), name='private_carousel_detail'),
  path('public/carousel/', PublicCarouselApi.as_view(), name='public_carousel'),
  path('public/carousel/<id_car>/', PublicCarouselDetailApi.as_view(), name='public_carousel_detail'),

]
