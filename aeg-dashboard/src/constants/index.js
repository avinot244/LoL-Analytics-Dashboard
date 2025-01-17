export const API_URL = "http://localhost:8000/api/"
export const roleList = ["Top", "Jungle", "Mid", "ADC", "Support"]
export const behaviorModelUUID = "976c4e70-ea03-11ee-ad17-00155da9b7d8"
export const MAP_WIDTH = 14750
export const MAP_HEIGHT = 14750

export const factorNamePerRole = {
        "Top": [
                "Playing with jungle",
                "Objective/Tower player",
                "Skirmish",
                "Farming safely",
                "Aggressive player",
                "Vision"
        ],
        "Jungle": [
                "Farming safely",
                "Invader",
                "Aggressive player",
                "Skirmish",
                "Playing botside",
                "playing topside"
        ],
        "Mid": [
                "Farming safely",
                "Aggressive player",
                "Objective/Tower player",
                "Roaming bot",
                "Skirmish",
                "Invader",
                "Roaming in jungle",
                "Roaming top"
        ],
        "ADC" : [
                "Aggressive player", 
                "Farmer", 
                "Lane player", 
                "Skirmish"
        ],
        "Support": [
                "Vision enemy jungle",
                "Vision ally jungle",
                "Generating difference",
                "Roaming mid",
                "Fighter/DPS",
                "Roaming top",
                "Playing with jungle"
        ]
        }

export const factorsPerRole = {"Top" : 6,
                         "Jungle" : 6,
                         "Mid" : 8,
                         "ADC" : 4,
                         "Support" : 7}
