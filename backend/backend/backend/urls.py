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

from behaviorADC.views import Topviews
from behaviorADC.views import Jungleviews
from behaviorADC.views import Midviews
from behaviorADC.views import ADCviews
from behaviorADC.views import Supportviews
from behaviorModels import views as behaviorModelsViews
from dataAnalysis import views as dataAnalysisViews
from Draft import views as draftViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # Behavior Top
    path('api/behavior/Top/getSummonnerList', Topviews.behaviorTop_get_player_list), # Getting the list of unique players
    path('api/behavior/Top/patch/update', Topviews.behaviorTop_updatePatch), # Updating patch values in the production database
    path('api/behavior/Top/stats/<str:summonnerName>', Topviews.behaviorTop_stats), # Getting stats of a given summonnerName
    path('api/behavior/Top/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Topviews.behaviorTop_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Top/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Topviews.behaviorTop_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Top/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_player), # Computing behavior analysis given a model and a player
    path('api/behavior/Top/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Top/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_patch), # Computing behavior analysis on a given patch for a given player and model

    # Behavior Jungle
    path('api/behavior/Jungle/getSummonnerList', Jungleviews.behaviorJungle_get_player_list), # Getting the list of unique players
    path('api/behavior/Jungle/patch/update', Jungleviews.behaviorJungle_updatePatch), # Updating patch values in the production database
    path('api/behavior/Jungle/stats/<str:summonnerName>', Jungleviews.behaviorJungle_stats), # Getting stats of a given summonnerName
    path('api/behavior/Jungle/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Jungleviews.behaviorJungle_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Jungle/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Jungleviews.behaviorJungle_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Jungle/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_player), # Computing behavior analysis given a model and a player
    path('api/behavior/Jungle/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Jungle/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_patch), # Computing behavior analysis on a given patch for a given player and model

    # Behavior Mid
    path('api/behavior/Mid/getSummonnerList', Midviews.behaviorMid_get_player_list), # Getting the list of unique players
    path('api/behavior/Mid/patch/update', Midviews.behaviorMid_updatePatch), # Updating patch values in the production database
    path('api/behavior/Mid/stats/<str:summonnerName>', Midviews.behaviorMid_stats), # Getting stats of a given summonnerName
    path('api/behavior/Mid/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Midviews.behaviorMid_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Mid/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Midviews.behaviorMid_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Mid/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_player), # Computing behavior analysis given a model and a player
    path('api/behavior/Mid/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Mid/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    
    # Behavior ADC
    path('api/behavior/ADC/getSummonnerList', ADCviews.behaviorADC_get_player_list), # Getting the list of unique players
    path('api/behavior/ADC/patch/update', ADCviews.behaviorADC_updatePatch), # Updating patch values in the production database
    path('api/behavior/ADC/stats/<str:summonnerName>', ADCviews.behaviorADC_stats), # Getting stats of a given summonnerName
    path('api/behavior/ADC/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', ADCviews.behaviorADC_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/ADC/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', ADCviews.behaviorADC_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/ADC/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_player), # Computing behavior analysis given a model and a player
    path('api/behavior/ADC/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/ADC/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_patch), # Computing behavior analysis on a given patch for a given player and model

    # Behavior Support
    path('api/behavior/Support/getSummonnerList', Supportviews.behaviorSupport_get_player_list), # Getting the list of unique players
    path('api/behavior/Support/patch/update', Supportviews.behaviorSupport_updatePatch), # Updating patch values in the production database
    path('api/behavior/Support/stats/<str:summonnerName>', Supportviews.behaviorSupport_stats), # Getting stats of a given summonnerName
    path('api/behavior/Support/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Supportviews.behaviorSupport_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Support/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Supportviews.behaviorSupport_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Support/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_player), # Computing behavior analysis given a model and a player
    path('api/behavior/Support/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Support/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    path('api/behavior/Support/deleteDuplicates', Supportviews.behaviorSupport_deleteDuplicates),
    
    # Behavior Models
    path('api/behaviorModels/<str:role>/getBestModel/', behaviorModelsViews.get_best_model),
    path('api/behaviorModels/<str:role>/computeModel', behaviorModelsViews.compute_model),
    path('api/behaviorModels/<str:uuid>/<str:role>/getModel/', behaviorModelsViews.get_model),

    # Data Analysis
    path('api/dataAnalysis/patch/getList', dataAnalysisViews.get_patch_list),
    path('api/dataAnalysis/tournament/getList', dataAnalysisViews.get_tournament_list),
    path('api/dataAnalysis/download/<str:rawTournamentList>/', dataAnalysisViews.download_latest),
    path('api/dataAnalysis/getTournamentMapping/', dataAnalysisViews.get_tournament_mapping),

    path('api/dataAnalysis/updateBins/', dataAnalysisViews.update_bins),
    path('api/dataAnalysis/deleteAllMeta/', dataAnalysisViews.delete_all_gameMetadata),

    # Draft
    path('api/draft/saveDrafts/', draftViews.saveDrafts),
]

