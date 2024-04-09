BEHAVIOR_ADC_HEADER = ["Date", "Tournament", "MatchId", "SeriesId", "Patch", "SummonnerName", "XPD@15", "GD@15", "CS/Min", "Kills", "Deaths", "Assists", "KP%", "Damage/Min", "JungleProximity", "botLanePresence", "riverBotPresence"]

API_URL = "http://localhost:8000/"

ROLE_LIST = ["Top" ,"Jungle", "Mid", "ADC", "Support"]

DATA_PATH = "./databases/"

BLACKLIST = ["2620486", # bugged game
             "2618289", # bugged game
             "2614989",
             "2615004",
             "2615009",
             "2615029",
             "2615050",
             "2615069",
             "2615148",
             "2615168",
             "2615176",
             "2615198",
             "2615220",
             "2615337",
             "2615348",
             "2615357",
             "2615365",
             "2615549",
             "2615606",
             "2617116",
             "2617116",
             "2617157",
             "2617208",
             "2619767",
             "2620761",
             "2620847",
             "2621136",
             "2621189",
             "2621197",
             "2622695",
             "2628766",
             "2616591",
             "2616647",
             "2617017",
             "2617053",
             "2620791",
             "2620812",
             "2620843",
             "2635729",
             "2616513",
             "2618273",
             "2617084", # bugged game
             
             
             
             "2662449",
             "2662447",
             "2624068",

            ] # upcoming match

factorsPerRole : dict = {"Top" : 6,
                         "Jungle" : 6,
                         "Mid" : 8,
                         "ADC" : 4,
                         "Support" : 7}
