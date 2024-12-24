from typing import Literal

item_destroyed_reason_types = Literal["sidegrade", "consume", "component", "other"]
summonner_spell_name_types = Literal["SummonerDot", "SummonerFlash", "SummonerSmite", "SummonerTeleport", "SummonerBoost", "SummonerFlashPerksHextechFlashtraptionV2", "S5_SummonerSmitePlayerGanker", "S12_SummonerTeleportUpgrade", "SummonerSmiteAvatarUtility", "SummonerHeal", "SummonerSmiteAvatarOffensive", "SummonerBarrier"]
champion_kill_types = Literal["firstBlood", "multi", "ace"]
channeling_types = Literal["recall", "skill", "summonerSpell"]
ward_types = Literal["yellowTrinket", "unknown", "control", "sight", "blueTrinket"]
monster_types = Literal["RedCamp", "BlueCamp", "Raptor", "Wolf", "Gromp", "Krug", "ScuttleCrab", "VoidGrub", "RiftHerald", "Baron"]
team_side_types = Literal["Order", "Chaos", "Unknown"]
epic_monster_kill_types = Literal["kill", "steal"]
dragon_types = Literal["air", "fire", "earth", "water", "chemtech", "hextech", "elder"]
epic_monster_types = Literal["dragon"]
lane_types = Literal["top", "bot", "mid"]
source_gold_grant_types = Literal["turretPlate", "turret", "inhibitor", "nexus"]
turret_tier_types = Literal["outer", "inner", "base", "nexus"]
building_types = Literal["turret", "inhibitor", "nexus"]
monster_names_types = Literal["Baron", "VoidGrub", "RiftHerald", "DragonWater", "DragonChemtech", "DragonHextech", "DragonFire", "DragonEarth", "DragonAir"]

event_types = Literal[
    "queued_epic_monster_info",
    "reconnect",
    "pause_ended",
    "queued_dragon_info",
    "item_purchased",
    "item_destroyed",
    "skill_level_up",
    "skill_used",
    "summoner_spell_used",
    "champion_kill",
    "champion_kill_special",
    "channeling_started",
    "item_active_ability_used",
    "ward_placed",
    "channeling_ended",
    "neutral_minion_spawn",
    "epic_monster_kill",
    "champion_level_up",
    "ward_killed",
    "epic_monster_spawn",
    "item_sold",
    "item_undo",
    "turret_plate_destroyed",
    "turret_plate_gold_earned",
    "building_gold_grant",
    "building_destroyed",
    "objective_bounty_prestart",
    "objective_bounty_finish"
]