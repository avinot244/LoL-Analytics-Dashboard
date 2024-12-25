from dataclasses import dataclass
from dataAnalysis.packages.Parsers.Separated.Events.LiteralTypes import *
from dataAnalysis.packages.Parsers.Separated.Events.Event import Event

@dataclass
class QueuedEpicMonsterInfoEvent(Event):
    gameTime : int
    monsterName: monster_names_types
    sequenceIndex : int
    spawnTime : int

@dataclass
class ReconnectEvent(Event):
    gameTime : int
    participant : int # participant Id
    sequenceIndex : int
    
@dataclass
class PauseEndedEvent(Event):
    gameTime : int
    sequenceIndex : int

@dataclass
class QueuedDragonInfoEvent(Event):
    gameTime : int
    nextDragonName: dragon_types
    nextDragonSpawnTime : int
    sequenceIndex : int

@dataclass
class ItemPurchasedEvent(Event):
    gameTime : int
    itemID : int
    participantID : int
    sequenceIndex : int 
    
@dataclass
class ItemDestroyedEvent(Event):
    gameTime : int
    itemID : int
    participantID : int
    sequenceIndex : int
    reason : item_destroyed_reason_types = None
    
@dataclass 
class SkillLevelUpEvent(Event):
    evolved : bool
    gameTime : int
    participant : int # participant ID
    sequenceIndex : int
    skillSlot : int
    
@dataclass
class SkillUsedEvent(Event):
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTime : int
    participant : int # participant ID
    sequenceIndex : int
    skillSlot : int
    
@dataclass
class SummonerSpellUsedEvent(Event):
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTime : int
    participantID : int
    summonerSpellName : summoner_spell_name_types
    summonerSpellSlot : int
    sequenceIndex : int
    
@dataclass
class ChampionKillEvent(Event):
    assistants : list[int]
    bounty : int
    deathRecap : list[dict]
    fightDuration : float
    gameTime : int
    killStreakLength : int
    killer : int # participant ID of the player that killer the player
    killerTeamID : int
    position : dict
    sequenceIndex : int
    victim : int # participant ID of the player that got killed
    victimTeamID : int
# "deathRecap": [
#     {
#         "breakdown": [
#             {
#                 "datadragonID": "SylasPassive",
#                 "isAutoAttack": false,
#                 "magicDmg": 141,
#                 "physicalDmg": 0,
#                 "trueDmg": 0
#             },
#             {
#                 "isAutoAttack": true,
#                 "magicDmg": 0,
#                 "physicalDmg": 146,
#                 "trueDmg": 0
#             },
#             {
#                 "datadragonID": "SylasE",
#                 "isAutoAttack": false,
#                 "magicDmg": 86,
#                 "physicalDmg": 0,
#                 "trueDmg": 0
#             }
#         ],
#         "casterId": 8,
#         "source": "Champion"
#     }
# ]

@dataclass
class ChampionKillSpecialEvent(Event):
    gameTime : int
    killType : champion_kill_types
    killer : int # participant ID of the player that killed
    position : dict
    sequenceIndex : int
    
@dataclass
class ChannelingStartedEvent(Event):
    channelingType : channeling_types
    gameTime : int
    inventorySlot : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class ItemActiveAbilityUsedEvent(Event):
    gameTime : int
    inventorySlot : int
    itemID : int
    maxCooldown : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class WardPlacedEvent(Event):
    gameTime : int
    placer : int
    position : dict
    sequenceIndex : int
    wardType: ward_types
    
@dataclass
class ChannelingEndedEvent(Event):
    channelingType : channeling_types
    gameTime : int
    inventorySlot : int
    isInterrupted : bool
    participantID : int
    sequenceIndex : int
    
@dataclass
class NeutralMinionSpawnEvent(Event):
    gameTime : int
    monsterType : monster_types
    position : dict
    sequenceIndex : int
    teamSide : team_side_types
    
@dataclass
class EpicMonsterKillEvent(Event):
    assistants : list[int] # List of participant IDs that helped killing said epic monster
    bountyGold : int
    gameTime : int
    inEnemyJungle : bool
    killType : epic_monster_kill_types
    killer : int # participant ID of the player that slayed said epic monster
    killerGold : int
    killerTeamID : int
    localGold : int
    monsterType : monster_types
    position : dict
    sequenceIndex : int
    
@dataclass
class ChampionLevelUpEvent(Event):
    gameTime : int
    level : int
    participant : int # participant ID of the player that leveled up
    sequenceIndex : int
    
@dataclass 
class WardKilledEvent(Event):
    gameTime : int
    killer : int # participant of ID who destroyed the ward
    position : dict
    sequenceIndex : int
    wardType : ward_types
    
@dataclass
class EpicMonsterSpawnEvent(Event):
    dragonType : dragon_types
    gameTime : int
    monsterType : epic_monster_types
    sequenceIndex : int
    
@dataclass
class ItemSoldEvent(Event):
    gameTime : int
    itemID : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class ItemUndoEvent(Event):
    gameTime : int
    goldGain : int
    itemID : int # item ID after undo
    participantID : int
    sequenceIndex : int
    itemAfterUndo : int = None
    itemBeforeUndo : int = None
    
@dataclass
class TurretPlateDestroyedEvent(Event):
    assistants : list[int] # list of participant ID that helped destroying the turret plate
    lane : lane_types
    lastHitter : int # participant ID who destoyed the plate
    position : dict
    sequenceIndex : int
    
@dataclass
class TurretPlateGoldEarnedEvent(Event):
    bounty : int
    gameTime : int
    participantID : int
    sequenceIndex : int
    teamID : int
    
@dataclass
class BuildingGoldGrantEvent(Event):
    amount : int
    position : dict
    recipientId : int
    sequenceIndex : int
    source : source_gold_grant_types
    teamID : int
    lane : lane_types = None
    turretTier : turret_tier_types = None # /!\ field value might not exist
    
@dataclass
class BuildingDestroyedEvent(Event): # parse more events building_destroyed
    assistants : list[int] # List of participant IDs that helped killing said building
    buildingType : building_types
    gameTime : int
    lane : lane_types
    lastHitter : int # participant ID that destroyed the tower
    position : dict
    sequenceIndex : int
    teamID : int
    bountyGold : int = None
    turretTier : turret_tier_types = None # /!\ field value might not exist

@dataclass 
class ObjectiveBountyPrestartEvent(Event):
    actualStartTime : int
    gameTime : int
    sequenceIndex : int
    teamID : int

@dataclass
class ObjectiveBountyFinishEvent(Event):
    gameTime : int
    sequenceIndex : int
    teamID : int