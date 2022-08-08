from enum import Enum
class PermissionsEnum(Enum):
    ADD_MIEMBRO= "api.add_miembro"
    VIEW_MIEMBRO= "api.view_miembro"
    CHANGE_MIEMBRO= "api.change_miembro"
    DELETE_MIEMBRO= "api.delete_miembro"
    
    ADD_PROYECTO= "api.add_proyecto"
    VIEW_PROYECTO= "api.view_proyecto"
    CHANGE_PROYECTO= "api.change_proyecto"
    DELETE_PROYECTO= "api.delete_proyecto"

    ADD_ARCHIVO= "api.add_archivo"
    VIEW_ARCHIVO= "api.view_archivo"
    CHANGE_ARCHIVO= "api.change_archivo"
    DELETE_ARCHIVO= "api.delete_archivo"
    
    ADD_USUARIO= "users.add_usuario"
    VIEW_USUARIO= "users.view_usuario"
    CHANGE_USUARIO= "users.change_usuario"
    DELETE_USUARIO= "users.delete_usuario"

    ADD_CONGRESO= "api.add_congreso"
    VIEW_CONGRESO= "api.view_congreso"
    CHANGE_CONGRESO= "api.change_congreso"
    DELETE_CONGRESO= "api.delete_congreso"

    ADD_PINTELECTUAL= "api.add_pintelectual"
    VIEW_PINTELECTUAL= "api.view_pintelectual"
    CHANGE_PINTELECTUAL= "api.change_pintelectual"
    DELETE_PINTELECTUAL= "api.delete_pintelectual"

    ADD_ARTICULO= "api.add_articulo"
    VIEW_ARTICULO= "api.view_articulo"
    CHANGE_ARTICULO= "api.change_articulo"
    DELETE_ARTICULO= "api.delete_articulo"

    ADD_TESIS= "api.add_tesis"
    VIEW_TESIS= "api.view_tesis"
    CHANGE_TESIS= "api.change_tesis"
    DELETE_TESIS= "api.delete_tesis"
    
    ADD_LIBRO= "api.add_libro"
    VIEW_LIBRO= "api.view_libro"
    CHANGE_LIBRO= "api.change_libro"
    DELETE_LIBRO= "api.delete_libro"

    ADD_CAROUSEL= "api.add_carousel"
    VIEW_CAROUSEL= "api.view_carousel"
    CHANGE_CAROUSEL= "api.change_carousel"
    DELETE_CAROUSEL= "api.delete_carousel"

    ADD_TEMA= "api.add_tema"
    VIEW_TEMA= "api.view_tema"
    CHANGE_TEMA= "api.change_tema"
    DELETE_TEMA= "api.delete_tema"

    ADD_CONTENTTYPE= "contenttypes.add_contenttype"
    VIEW_CONTENTTYPE= "contenttypes.view_contenttype"
    CHANGE_CONTENTTYPE= "contenttypes.change_contenttype"
    DELETE_CONTENTTYPE= "contenttypes.delete_contenttype"
    
    ADD_GROUP= "auth.add_group"
    VIEW_GROUP= "auth.view_group"
    CHANGE_GROUP= "auth.change_group"
    DELETE_GROUP= "auth.delete_group"

    ADD_TOKENPROXY= "authtoken.add_tokenproxy"
    VIEW_TOKENPROXY= "authtoken.view_tokenproxy"
    CHANGE_TOKENPROXY= "authtoken.change_tokenproxy"
    DELETE_TOKENPROXY= "authtoken.delete_tokenproxy"

    ADD_PERMISSION= "auth.add_permission"
    VIEW_PERMISSION= "auth.view_permission"
    CHANGE_PERMISSION= "auth.change_permission"
    DELETE_PERMISSION= "auth.delete_permission"
    
    ADD_LOGENTRY= "admin.add_logentry"
    VIEW_LOGENTRY= "admin.view_logentry"
    CHANGE_LOGENTRY= "admin.change_logentry"
    DELETE_LOGENTRY= "admin.delete_logentry"

    ADD_TOKEN= "authtoken.add_token"
    VIEW_TOKEN= "authtoken.view_token"
    CHANGE_TOKEN= "authtoken.change_token"
    DELETE_TOKEN= "authtoken.delete_token"

    ADD_SESSION= "sessions.add_session"
    VIEW_SESSION= "sessions.view_session"
    CHANGE_SESSION= "sessions.change_session"
    DELETE_SESSION= "sessions.delete_session"