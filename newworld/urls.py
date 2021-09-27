"""newworld URL Configuration

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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from newworldapi.views import *
from django.views import generic
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet, 'posts')
router.register(r'messages', MessageViewSet, 'messages')
router.register(r'factions', FactionViewSet, 'factions')
router.register(r'settlements', SettlementViewSet, 'settlements')
router.register(r'gameusers', GameusersViewSet, 'gameusers')
router.register(r'servers', ServerViewSet, 'servers')
router.register(r'items', ItemViewSet, 'items')


urlpatterns = [
    path("", generic.TemplateView.as_view(template_name="home.html")),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]