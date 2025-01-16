# pickRate + banRate / 2 = presenceRate => valuable
# Sélectionner plusieurs 
# Regrouper les requêtes dans une seule requête GraphQL

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
from django.urls import path, re_path, include

from behaviorADC.views import Topviews
from behaviorADC.views import Jungleviews
from behaviorADC.views import Midviews
from behaviorADC.views import ADCviews
from behaviorADC.views import Supportviews
from behaviorModels import views as behaviorModelsViews
from dataAnalysis import views as dataAnalysisViews
from dataAnalysis import viewsTeam as teamAnalysisViews
from Draft import views as draftViews
from authentication import views as authenticationViews
from Monitoring import views as monitoringViews


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Behavior Top
    path('api/behavior/Top/getSummonnerList/<str:patch>/<int:scrim>/', Topviews.behaviorTop_get_player_list), # Getting the list of unique players
    path('api/behavior/Top/getSummonnerListTournament/<str:patch>/<str:tournament>/', Topviews.behaviorTop_get_player_list_tournament), # Getting the list of unique players
    path('api/behavior/Top/patch/update', Topviews.behaviorTop_updatePatch), # Updating patch values in the production database
    path('api/behavior/Top/stats/<str:summonnerName>', Topviews.behaviorTop_stats), # Getting stats of a given summonnerName
    path('api/behavior/Top/stats/<str:summonnerName>/<str:tournament>/', Topviews.behaviorTop_stats_tournament),
    
    path('api/behavior/Top/stats/game/<str:summonnerName>/<int:seriesId>/<int:gameNumber>/', Topviews.behaviorTop_stats_game),
    
    path('api/behavior/Top/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Topviews.behaviorTop_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Top/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Topviews.behaviorTop_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Top/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Top/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    
    path('api/behavior/Top/compute/<str:summonnerName>/<str:uuid>/<int:seriesId>/<int:gameNumber>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_game),
    path('api/behavior/Top/compute/singleGamesLatest/<str:summonnerName>/<str:uuid>/<int:limit>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_singleGamesLatest),
    
    path('api/behavior/Top/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Topviews.behaviorTop_behavior_tournament),
    path('api/behavior/Top/computeScouting/', Topviews.behaviorTop_behavior_multiple_tournaments),


    # Behavior Jungle
    path('api/behavior/Jungle/getSummonnerList/<str:patch>/<int:scrim>/', Jungleviews.behaviorJungle_get_player_list), # Getting the list of unique players
    path('api/behavior/Jungle/getSummonnerListTournament/<str:patch>/<str:tournament>/', Jungleviews.behaviorJungle_get_player_list_tournament), # Getting the list of unique players
    path('api/behavior/Jungle/patch/update', Jungleviews.behaviorJungle_updatePatch), # Updating patch values in the production database
    path('api/behavior/Jungle/stats/<str:summonnerName>', Jungleviews.behaviorJungle_stats), # Getting stats of a given summonnerName
    path('api/behavior/Jungle/stats/<str:summonnerName>/<str:tournament>/', Jungleviews.behaviorJungle_stats_tournament),
    
    path('api/behavior/Jungle/stats/game/<str:summonnerName>/<int:seriesId>/<int:gameNumber>/', Jungleviews.behaviorJungle_stats_game),
    
    path('api/behavior/Jungle/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Jungleviews.behaviorJungle_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Jungle/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Jungleviews.behaviorJungle_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Jungle/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Jungle/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    
    path('api/behavior/Jungle/compute/<str:summonnerName>/<str:uuid>/<int:seriesId>/<int:gameNumber>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_game),
    path('api/behavior/Jungle/compute/singleGamesLatest/<str:summonnerName>/<str:uuid>/<int:limit>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_singleGamesLatest),
    
    path('api/behavior/Jungle/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Jungleviews.behaviorJungle_behavior_tournament),
    path('api/behavior/Jungle/computeScouting/', Jungleviews.behaviorJungle_behavior_multiple_tournaments),


    # Behavior Mid
    path('api/behavior/Mid/getSummonnerList/<str:patch>/<int:scrim>/', Midviews.behaviorMid_get_player_list), # Getting the list of unique players
    path('api/behavior/Mid/getSummonnerListTournament/<str:patch>/<str:tournament>/', Midviews.behaviorMid_get_player_list_tournament), # Getting the list of unique players
    path('api/behavior/Mid/patch/update', Midviews.behaviorMid_updatePatch), # Updating patch values in the production database
    path('api/behavior/Mid/stats/<str:summonnerName>', Midviews.behaviorMid_stats), # Getting stats of a given summonnerName
    path('api/behavior/Mid/stats/<str:summonnerName>/<str:tournament>/', Midviews.behaviorMid_stats_tournament),
    
    path('api/behavior/Mid/stats/game/<str:summonnerName>/<int:seriesId>/<int:gameNumber>/', Midviews.behaviorMid_stats_game),
    
    path('api/behavior/Mid/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Midviews.behaviorMid_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Mid/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Midviews.behaviorMid_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Mid/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Mid/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    
    path('api/behavior/Mid/compute/<str:summonnerName>/<str:uuid>/<int:seriesId>/<int:gameNumber>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_game),
    path('api/behavior/Mid/compute/singleGamesLatest/<str:summonnerName>/<str:uuid>/<int:limit>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_singleGamesLatest),
    
    path('api/behavior/Mid/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Midviews.behaviorMid_behavior_tournament),
    path('api/behavior/Mid/computeScouting/', Midviews.behaviorMid_behavior_multiple_tournaments),


    # Behavior ADC
    path('api/behavior/ADC/getSummonnerList/<str:patch>/<int:scrim>/', ADCviews.behaviorADC_get_player_list), # Getting the list of unique players
    path('api/behavior/ADC/getSummonnerListTournament/<str:patch>/<str:tournament>/', ADCviews.behaviorADC_get_player_list_tournament), # Getting the list of unique players
    path('api/behavior/ADC/patch/update', ADCviews.behaviorADC_updatePatch), # Updating patch values in the production database
    path('api/behavior/ADC/stats/<str:summonnerName>', ADCviews.behaviorADC_stats), # Getting stats of a given summonnerName
    path('api/behavior/ADC/stats/<str:summonnerName>/<str:tournament>/', ADCviews.behaviorADC_stats_tournament),

    path('api/behavior/ADC/stats/game/<str:summonnerName>/<int:seriesId>/<int:gameNumber>/', ADCviews.behaviorADC_stats_game),

    path('api/behavior/ADC/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', ADCviews.behaviorADC_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/ADC/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', ADCviews.behaviorADC_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/ADC/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/ADC/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    
    path('api/behavior/ADC/compute/<str:summonnerName>/<str:uuid>/<int:seriesId>/<int:gameNumber>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_game),
    path('api/behavior/ADC/compute/singleGamesLatest/<str:summonnerName>/<str:uuid>/<int:limit>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_singleGamesLatest),


    path('api/behavior/ADC/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', ADCviews.behaviorADC_behavior_tournament),
    path('api/behavior/ADC/computeScouting/', ADCviews.behaviorADC_behavior_multiple_tournaments),



    # Behavior Support
    path('api/behavior/Support/getSummonnerList/<str:patch>/<int:scrim>/', Supportviews.behaviorSupport_get_player_list), # Getting the list of unique players
    path('api/behavior/Support/getSummonnerListTournament/<str:patch>/<str:tournament>/', Supportviews.behaviorSupport_get_player_list_tournament), # Getting the list of unique players
    path('api/behavior/Support/patch/update', Supportviews.behaviorSupport_updatePatch), # Updating patch values in the production database
    path('api/behavior/Support/stats/<str:summonnerName>', Supportviews.behaviorSupport_stats), # Getting stats of a given summonnerName
    path('api/behavior/Support/stats/<str:summonnerName>/<str:tournament>/', Supportviews.behaviorSupport_stats_tournament),
    
    path('api/behavior/Support/stats/game/<str:summonnerName>/<int:seriesId>/<int:gameNumber>/', Supportviews.behaviorSupport_stats_game),
    
    path('api/behavior/Support/stats/latest/<str:summonnerName>/<int:limit>/<str:tournament>/', Supportviews.behaviorSupport_stats_latest), # Getting last limit stats of a given summonnerName
    path('api/behavior/Support/stats/patch/<str:summonnerName>/<str:patch>/<str:tournament>/', Supportviews.behaviorSupport_stats_patch), # Getting patch stats of a given summonnerName
    path('api/behavior/Support/compute/<str:summonnerName>/<int:limit>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_latest), # Computing latest behavior analysis given a model and a player
    path('api/behavior/Support/compute/<str:summonnerName>/<str:patch>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_patch), # Computing behavior analysis on a given patch for a given player and model
    path('api/behavior/Support/compute/<str:summonnerName>/<str:uuid>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_tournament),
    
    path('api/behavior/Support/compute/<str:summonnerName>/<str:uuid>/<int:seriesId>/<int:gameNumber>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_game),
    path('api/behavior/Support/compute/singleGamesLatest/<str:summonnerName>/<str:uuid>/<int:limit>/<str:wantedTournament>/<str:comparisonTournament>/', Supportviews.behaviorSupport_behavior_singleGamesLatest),

    path('api/behavior/Support/deleteDuplicates', Supportviews.behaviorSupport_deleteDuplicates),
    path('api/behavior/Support/computeScouting/', Supportviews.behaviorSupport_behavior_multiple_tournaments),
    
    # Behavior Models
    path('api/behaviorModels/<str:role>/getBestModel/', behaviorModelsViews.get_best_model),
    path('api/behaviorModels/<str:role>/computeModel', behaviorModelsViews.compute_model),
    path('api/behaviorModels/<str:uuid>/<str:role>/getModel/', behaviorModelsViews.get_model),
    path('api/behaviorModels/getLoadingMatrix/<str:uuid>/<str:role>/', behaviorModelsViews.get_loading_matrix),
    path('api/behaviorModels/deleteAllMetadata/', behaviorModelsViews.deleteAllModelsMetadata),
    path('api/behaviorModels/getAll/', behaviorModelsViews.get_all_models),
    path('api/behaviorModels/delete/<str:uuid>/<str:role>/', behaviorModelsViews.deleteModel),
    path('api/behaviorModels/setActive/<str:uuid>/<str:role>/', behaviorModelsViews.setModelAsActive),
    path('api/behaviorModels/setFactorsName/<str:uuid>/<str:role>/', behaviorModelsViews.setFactorsName),
    path('api/behaviorModels/getModel/<str:role>/', behaviorModelsViews.getModel),
    path('api/behaviorModels/generateLoadings/', behaviorModelsViews.generate_loadings),
    path('api/behaviorModels/getRegionSplit/<str:uuid>/<str:role>/', behaviorModelsViews.getRegionSplit),

    # Data Analysis
    path('api/behavior/deleteAll/', dataAnalysisViews.delete_all_behavior),
    path('api/dataAnalysis/deleteGame/<int:seriesId>/<int:gameNumber>/', dataAnalysisViews.deleteGame),
    path('api/dataAnalysis/tournament/<str:summonnerName>/<str:patch>/<int:scrim>/', dataAnalysisViews.getTournamentFromPlayer),
    path('api/dataAnalysis/patch/getList/<int:scrim>/', dataAnalysisViews.get_patch_list),
    path('api/dataAnalysis/tournament/getList', dataAnalysisViews.get_tournament_list),
    path('api/dataAnalysis/tournament/getDict', dataAnalysisViews.get_tournament_dict),
    path('api/dataAnalysis/download/<str:rawTournamentList>/', dataAnalysisViews.download_latest),
    path('api/dataAnalysis/getTournamentMapping/', dataAnalysisViews.get_tournament_mapping),

    path('api/dataAnalysis/deleteAllMeta/', dataAnalysisViews.delete_all_gameMetadata),
    path('api/dataAnalysis/patch/getFromTournament/<str:tournament>/', dataAnalysisViews.getPatchListFromTournament),

    path('api/dataAnalysis/computeBehaviorStats/<int:time>/', dataAnalysisViews.computeNewBehaviorStats),
    path('api/dataAnalysis/deleteAllBehaviorStats/', dataAnalysisViews.deleteAllBehaviorStats),

    path('api/dataAnalysis/getListDownlodableTournament/<int:year>/', dataAnalysisViews.getListOfDownloadableTournament),
    path('api/dataAnalysis/getTournamentListShortened/', dataAnalysisViews.get_tournament_list_shortened),
    path('api/dataAnalysis/refreshTournamentDownloadable/', dataAnalysisViews.refreshTournamentDownloadable),


    path('api/dataAnalysis/updateDatabase/<str:tournamentList>/', dataAnalysisViews.updateDatabase),

    path('api/dataAnalysis/getGameList/<str:tournament>/', dataAnalysisViews.getGameList),

    path('api/dataAnalysis/getGamePositionDensity/', dataAnalysisViews.getGamePositionDensity),
    path('api/dataAnalysis/gameAnalysis/players/<int:seriesId>/<int:gameNumber>/', dataAnalysisViews.getGameStatsPlayers),
    path('api/dataAnalysis/gameAnalysis/teams/<int:seriesId>/<int:gameNumber>/', dataAnalysisViews.getGameStatsTeams),

    path('api/dataAnalysis/getProximityMatrix/<int:seriesId>/<int:gameNumber>/<int:time>/', dataAnalysisViews.getProximityMatrix),
    path('api/dataAnalaysis/getGameEvents/', dataAnalysisViews.getGameEvents),
    
    # Team Analysis
    path('api/teamAnalysis/getAllTeams/', teamAnalysisViews.getTeamList),
    path('api/teamAnalysis/getTournamentsFromTeam/<str:team>/', teamAnalysisViews.getTournamentsFromTeam),
    path('api/teamAnalysis/getPlayerPosition/', teamAnalysisViews.getPlayerPosition),
    path('api/teamAnalysis/getResetPositions/', teamAnalysisViews.getPlayerResetPositions),
    path('api/teamAnalysis/getWardPositions/', teamAnalysisViews.getWardPlacedPositions),
    path('api/teamAnalysis/getGrubsDrakesStats/', teamAnalysisViews.getGrubsDrakeStats),
    path('api/teamAnalysis/getFirstTowerHeraldData/', teamAnalysisViews.getFirstTowerHeraldStats),
    path('api/teamAnalysis/getHeraldData/', teamAnalysisViews.getHeraldData),
    path('api/teamAnalysis/getFirstTowerData/', teamAnalysisViews.getFirstTowerData),


    # Draft
    path('api/draft/saveDrafts/', draftViews.saveDrafts),
    path('api/draft/getLatest/<int:limit>/<int:scrimStr>/', draftViews.getLatestDraft),
    path('api/draft/getPatch/<str:patch>/<int:scrimStr>/', draftViews.getDraftPatch),
    path('api/draft/getTournament/<str:tournament>/', draftViews.getDraftTournament),
    path('api/draft/getChampion/<str:championName>/<str:patch>/', draftViews.getDraftChampion),
    path('api/draft/getTeamNames/<int:seriesId>/<int:gameNumber>/', draftViews.getTeamNames),
    path('api/draft/getDraftGame/<int:seriesId>/<int:gameNumber>/', draftViews.getDraftGame),
    path('api/draft/delete/', draftViews.deleteAllDrafts),

    path('api/draft/championStats/updateStats/<str:tournamentListStr>/', draftViews.updateChampionDraftStats),
    path('api/draft/championStats/getStats/<str:patch>/<str:side>/<str:tournament>/', draftViews.getChampionDraftStats),
    path('api/draft/championStats/getBans/<str:patch>/<str:side>/<str:tournament>/', draftViews.getChampionDraftBans),

    path('api/draft/championStats/deleteChampionGameStats/', draftViews.deleteAllChampionDraftStats),
    path('api/draft/championStats/deleteChampionBansStats/', draftViews.deleteAllChampionBansStats), 

    path('api/draft/championStats/getTopChampions/<str:role>/<str:filter>/<str:side>/<str:patch>/<str:tournament>/', draftViews.getTopChampions),

    path('api/draft/updatePlayerStat/<str:tournamentListStr>/', draftViews.updatePlayerStats),
    path('api/draft/playerStat/<str:summonnerName>/<str:tournament>/<str:filter>/', draftViews.getPlayerStats),
    path('api/draft/playerStat/deleteAll/', draftViews.deleteAllChampionPool),
    path('api/draft/deleteSingleGame/<int:seriesId>/<int:gameNumber>/', draftViews.deleteDraftStatSingleGame),

    # Authentication
    path("api/authentication/login/", authenticationViews.loginUser, name="api_login"),
    path("api/authentication/logout/", authenticationViews.logoutUser, name="api_logout"),
    path("api/authentication/session/", authenticationViews.session_view, name="api_session"),
    path("api/authentication/whoami/", authenticationViews.whomai_view, name="api_whoami"),
    path("api/authentication/getUserList/", authenticationViews.getUserList),
    path("api/authentication/deleteUser/<str:username>/", authenticationViews.deleteUser),
    path('api/token/auth/', include('rest_framework.urls')),
    path('api/token/getPair/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/authentication/test', authenticationViews.test),
    
    # Monitoring
    path("api/monitoring/refresh/<str:dbName>/", monitoringViews.refresh_db),
]

