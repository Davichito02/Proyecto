from users.models import *
from datetime import datetime
from public.views import FIELD_USERNAME
from accounts.serializers import UsuarioSerializer
from authentication.serializers import LogoutSerializer
from django.http import HttpResponseRedirect
from django.contrib.auth import SESSION_KEY
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer

def succes_response(msg, token, user_serializer, user, status):
    return Response({'error': False,'msg': msg, 'data': {
            'token': token.key,
            'user': user_serializer.data,
            'permissions': user.get_all_permissions()
        }}, status = status)

def logout_all(user):
    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
    if all_sessions.exists():
        for session in all_sessions:
            session_data = session.get_decoded()
            if str(user.id) == str(session_data.get(SESSION_KEY)):
                session.delete()

class Login(ObtainAuthToken):
    http_method_names = ['get', 'post', 'options']

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user= request.user
        if request.method=='GET':
            if user.is_authenticated:
                succes_url= "/accounts/profile/"
                token = Token.objects.filter(user = user).first()
                if token:
                    return HttpResponseRedirect(succes_url)
                else:
                    logout_all(user)
                    return super(Login, self).dispatch(request, *args, **kwargs)
            else: 
                return super(Login, self).dispatch(request, *args, **kwargs)
        else:
            if user.is_authenticated:
                logout(request)
            return super(Login, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwars):
        return Response({'msg':'Ingrese sus credenciales de acceso. Su '+ FIELD_USERNAME +' y contraseña'}, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.is_active:
                self.serializer_class = UsuarioSerializer
                user_serializer = self.get_serializer(user)
                self.serializer_class = AuthTokenSerializer
                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    logout_all(user)
                    token.delete()
                    token = Token.objects.create(user = user)
                    #return Response({'error': True, 'msg': 'Ya se ha iniciado sesión con este usuario.', 'data': None}, status = status.HTTP_409_CONFLICT)
                if not request.user.is_authenticated:
                    login(request, user)
                return succes_response('Succes Login!', token, user_serializer, user, status.HTTP_201_CREATED)
                #succes_url= "/accounts/detail/"+str(user.id)
                #return HttpResponseRedirect(succes_url)
            else:
                return Response({'error': True, 'msg': 'Su cuenta se encuentra bloqueada.', 'data': None}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': True, 'msg': FIELD_USERNAME.capitalize()+ ' y contraseña icorrectos.', 'data': None}, status = status.HTTP_400_BAD_REQUEST)

class Logout(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'options']

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user= request.user
        if request.method=='GET':
            succes_url= "/auth/login/"
            if not user.is_authenticated:
                return HttpResponseRedirect(succes_url)
            else:
                token = Token.objects.filter(user = user).first()
                if token:
                    return super(Logout, self).dispatch(request, *args, **kwargs)
                else:
                    logout(request)
                    return HttpResponseRedirect(succes_url)
        else:
            return super(Logout, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwars):
        token = Token.objects.filter(user = request.user).first()
        if token:
            return Response({'msg':'Enviar su clave de token de usuario para cerrar la sesión.', 'user': str(token.user), 'token': str(token)}, status = status.HTTP_200_OK)
        return Response({'msg':'Ya se encuentra cerrada su sesión.'}, status = status.HTTP_409_CONFLICT)

    def post(self, request, *args, **kwars):
        try:
            token = request.data['key']
            #request.user.auth_token.delete()
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user
                if(user.is_authenticated):
                    logout(request)
                logout_all(user)
                token.delete()
                return Response({'error': False, 'msg': 'Sesión cerrada.'}, status = status.HTTP_200_OK)
            return Response({'error': True, 'msg': 'Error al cerrar la sesión. Token inválido'}, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': True, 'msg': 'No se ha encontrado el token en la petición.'}, status = status.HTTP_409_CONFLICT)

class SignUp(generics.CreateAPIView):
    parser_class = (FileUploadParser,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    http_method_names = ['get', 'post', 'options']

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user= request.user
        if request.method=='GET':
            if user.is_authenticated:
                succes_url= "/accounts/profile/"
                token = Token.objects.filter(user = user).first()
                if token:
                    return HttpResponseRedirect(succes_url)
                else:
                    logout(request)
                    return super(SignUp, self).dispatch(request, *args, **kwargs)
            else: 
                return super(SignUp, self).dispatch(request, *args, **kwargs)
        else:
            if user.is_authenticated:
                logout(request)
            return super(SignUp, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwars):
        return Response({'msg':'Registrarse.'}, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        register = self.get_serializer(data=request.data)
        if register.is_valid():
            user = register.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            return Response({'error': False, 'msg': 'Cuenta registrada correctamente.', 'data': register.data}, status = status.HTTP_201_CREATED)
        else:
            return Response({'error': True, 'msg': register.errors, 'data': None}, status = status.HTTP_400_BAD_REQUEST)
