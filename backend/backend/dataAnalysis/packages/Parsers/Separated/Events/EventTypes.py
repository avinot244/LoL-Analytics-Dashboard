from dataclasses import dataclass
from dataAnalysis.packages.utils_stuff.Position import Position
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
    participantID : int
    sequenceIndex : int
    
@dataclass
class PauseEndedEvent(Event):
    gameTime : int
    sequenceIndex : int

@dataclass
class QueuedDragonInfoEvent(Event):
    gameTime : int
    nextDragonName: dragon_types
    nexDragonSpawnTime : int
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
    reason : item_destroyed_reason_types
    sequenceIndex : int
    
@dataclass 
class SkillLevelUpEvent(Event):
    evolved : bool
    gameTime : int
    participantID : int
    seqeuenceIndex : int
    skillSlot : int
    
@dataclass
class SkillUsedEvent(Event):
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTime : int
    participantId : int
    sequenceIndex : int
    skillSlot : int
    
@dataclass
class SummonnerSpellUsedEvent(Event):
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTume : int
    participantID : int
    summonnerSpellName : summonner_spell_name_types
    summonnerSpellSlot : int
    
    
@dataclass
class ChampionKillEvent(Event):
    assistants : list[int]
    bounty : int
    deathRecap : list[dict]
    fightDuration : float
    gameTime : int
    killStreakLength : int
    killerID : int
    killerTeamID : int
    position : Position
    sequenceIndex : int
    victimID : int
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
    killerID : int
    position : Position
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
    placerID : int
    position : Position
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
    position : Position
    sequenceIndex : int
    teamSide : team_side_types
    
@dataclass
class EpicMonsterKillEvent(Event): #parse more events epic_monster_kill
    assistants : list[int] # List of participant IDs that helped killing said epic monster
    bountyGold : int
    gameTime : int
    inEnemyJungle : bool
    killType : epic_monster_kill_types
    killerID : int
    killerGold : int
    killerTeamID : int
    localGold : int
    monsterType : monster_types
    position : Position
    sequenceIndex : int
    
@dataclass
class ChampionLevelUpEvent(Event):
    gameTime : int
    level : int
    participantID : int
    sequenceIndex : int
    
@dataclass 
class WardKilledEvent(Event):
    gameTime : int
    killerID : int
    position : Position
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
    itemIDAfterUndo : int
    itemID : int
    particpantID : int
    sequenceIndex : int
    
@dataclass
class TurretPlateDestroyedEvent(Event):
    lane : lane_types
    lastHitterID : int
    position : Position
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
    lane : lane_types
    position : Position
    recipientID : int
    sequenceIndex : int
    source : source_gold_grant_types
    teamID : int
    turretTier : turret_tier_types # /!\ field value might not exist
    
@dataclass
class BuildingDestroyedEvent(Event): # parse more events building_destroyed
    assistants : list[int] # List of participant IDs that helped killing said building
    bountyGold : int
    buildingType : building_types
    gameTime : int
    lane : lane_types
    lastHitterID : int
    position : Position
    sequenceIndex : int
    teamID : int
    turretTier : turret_tier_types # /!\ field value might not exist

@dataclass 
class ObjectiveBountyPrestartEvent(Event):
    actualStartTime : int
    gameTime : int
    sequenceIndex : int
    teamID : int

@dataclass
class ObjectiveBountyFinishedEvent(Event):
    gameTime : int
    sequenceIndex : int
    teamID : int