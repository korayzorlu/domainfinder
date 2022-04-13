"""mrblog URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from finder.views import index, addRow, deleteRow, DomainViewSet
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.contrib.auth import views as auth_views

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router = routers.DefaultRouter()
router.register(r'domains', DomainViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = "index"),
    path('add/<str:name>', addRow, name = "addRow"),
    path('delete/<str:list>', deleteRow, name = "deleteRow"),
    path('restapi/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]