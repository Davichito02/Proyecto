from accounts.views import *
from django.urls import path

urlpatterns = [
  path('profile/', ProfileView.as_view(), name='profile'),
  path('detail/<id>/', UserDetailApi.as_view(), name='detail'),
  path('credentials/<id>/', UserUpdateCredentials.as_view(), name='credentials'),
]