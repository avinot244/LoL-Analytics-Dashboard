from dataclasses import dataclass

from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.Parsers.Separated.Events.LiteralTypes import item_destroyed_reason_types

@dataclass
class ItemPurchasedEvent():
    gameTime : int
    itemID : int
    participantID : int
    sequenceIndex : int 
    
@dataclass
class ItemDestroyedEvent():
    gameTime : int
    itemID : int
    participantID : int
    reason : item_destroyed_reason_types
    sequenceIndex : int
    
@dataclass 
class SkillLevelUpEvent():
    evolved : bool
    gameTime : int
    participantID : int
    seqeuenceIndex : int
    skillSlot : int
    
@dataclass
class SkillUsedEvent():
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTime : int
    participantId : int
    sequenceIndex : int
    skillSlot : int
    
@dataclass
class SummonnerSpellUsedEvent():
    chargesRemaining : int
    gameTime : int
    maxCharges : int
    maxCooldown : int
    maxRechargeTume : int
    participantID : int
    summonnerSpellName : str # add Literal typing
    summonnerSpellSlot : int
    
    
@dataclass
class ChampionKillEvent():
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
class ChampionKillSpecialEvent():
    gameTume : int
    killType : str # add Literal typing
    killerID : int
    position : Position
    sequenceIndex : int
    
@dataclass
class ChannelingStartedEvent():
    channelingType : str # add Literal typing
    gameTime : int
    inventorySlot : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class ItemActiveAbilityUsedEvent():
    gameTime : int
    inventorySlot : int
    itemID : int
    maxCooldown : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class WardPlacedEvent():
    gameTime : int
    placerID : int
    position : Position
    sequenceIndex : int
    wardType: str # add Literal typing
    
@dataclass
class ChannelingEndedEvent():
    channelingType : str # add Literal typing
    gameTime : int
    inventorySlot : int
    isInterrupted : bool
    participantID : int
    sequenceIndex : int
    
@dataclass
class NeutralMinionSpawnEvent():
    gameTime : int
    monsterType : str # add Literal typing
    position : Position
    sequenceIndex : int
    teamSide : str # add Literal typing
    
@dataclass
class EpicMonsterKillEvent(): #parse more events epic_monster_kill
    assistants : list
    bountyGold : int
    gameTime : int
    inEnemyJungle : bool
    killType : str # add Literal typing
    killerID : int
    killerGold : int
    killerTeamID : int
    localGold : int
    monsterType : str # add Literal typing
    position : Position
    sequenceIndex : int
    
@dataclass
class ChampionLevelUPEvent():
    gameTime : int
    level : int
    participantID : int
    sequenceIndex : int
    
@dataclass 
class WardKilledEvent():
    gameTime : int
    killerID : int
    position : Position
    sequenceIndex : int
    wardType : str # add Literal typing
    
@dataclass
class EpicMonsterSpawnEvent():
    dragonType : str # add Literal typing
    gameTime : int
    monsterType : str # add Literal typing
    sequenceIndex : int
    
@dataclass
class ItemSoldEvent():
    gameTime : int
    itemID : int
    participantID : int
    sequenceIndex : int
    
@dataclass
class ItemUndoEvent():
    gameTime : int
    goldGain : int
    itemIDAfterUndo : int
    itemID : int
    particpantID : int
    sequenceIndex : int
    
@dataclass
class TurretPlateDestroyedEvent():
    lane : str # add Literal typing
    lastHitterID : int
    position : Position
    sequenceIndex : int
    
@dataclass
class TurretPlateGoldEarnedEvent():
    bounty : int
    gameTime : int
    participantID : int
    sequenceIndex : int
    teamID : int
    
@dataclass
class BuildingGoldGrantEvent():
    amount : int
    lane : str # add Literal typing
    position : Position
    recipientID : int
    sequenceIndex : int
    source : str # add Literal typing
    teamID : int
    turretTier : str # add Literal typing
    
@dataclass
class BuildingDestroyedEvent(): # parse more events building_destroyed
    assistants : list
    bountyGold : int
    buildingType : str # add Literal typing
    gameTime : int
    lane : str # add Literal typing
    lastHitterID : int
    position : Position
    sequenceIndex : int
    teamID : int
    turretTier : str # add Literal typing

@dataclass 
class ObjectiveBOuntyPrestartEvent():
    actualStartTime : int
    gameTime : int
    sequenceIndex : int
    teamID : int

@dataclass
class ObjectiveBountyFInishedEvent():
    gameTime : int
    sequenceIndex : int
    teamID : int
