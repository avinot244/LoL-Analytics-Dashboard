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
from behaviorADC import views as ADCviews
from dataAnalysis import views as dataAnalysisViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # Behavior ADC
    path('api/behavior/ADC/getSummonnerList', ADCviews.behaviorADC_get_player_list), # Getting the list of unique players
    re_path(r'^api/behavior/ADC/patch/update', ADCviews.behaviorADC_updatePatch), # Updating patch value sin the production database
    path('api/behavior/ADC/stats/<str:summonnerName>', ADCviews.behaviorADC_stats), # Getting stats of a given summonnerName
    path('api/behavior/ADC/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>', ADCviews.behaviorADC_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/ADC/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>', ADCviews.behaviorADC_stats_patch), # Getting patch stats of a given summonnerName
    



    path('api/dataAnalysis/patch/getList', dataAnalysisViews.get_patch_list),
    path('api/dataAnalysis/tournament/getList', dataAnalysisViews.get_tournament_list),
    path('api/dataAnalysis/download/<str:rawTournamentList>/', dataAnalysisViews.download_latest),
    path('api/dataAnalysis/getTournamentMapping/', dataAnalysisViews.get_tournament_mapping),
]