"""
URL configuration for django_tests_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from behaviorADC import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/behavior/ADC/latest/([0-9]*)$', views.behaviorADC_latest),

    re_path(r'^api/behavior/ADC/patch/getList', views.get_listPatch),
    re_path(r'^api/behavior/ADC/patch/update', views.behaviorADC_updatePatch),
    path('api/behavior/ADC/stats/<str:summonnerName>', views.behaviorADC_stats),
    path('api/behavior/ADC/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>', views.behaviorADC_stats_latest),
    path('api/behavior/ADC/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>', views.behaviorADC_stats_patch),
]