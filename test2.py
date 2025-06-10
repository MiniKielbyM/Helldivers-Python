Scavenger = ["Scavenger", "SV", True, 5, 0, False, 0, 0, 0, 5, 5, 10, 0, 10]
Pouncer = ["Pouncer", "PC", True, 5, 0, False, 0, 0, 0, 5, 10, 15, 0, 15]
Hunter = ["Hunter", "HT", True, 10, 1, False, 0, 0, 0, 5, 5, 10, 5, 10]
Hive_Guard = ["Hive Guard", "HG", True, 5, 0, False, 0, 0, 0, 2, 5, 15, 30, 15]
Charger = ["Charger", "CR", True, 30, 20, False, 0, 0, 0, 10, 5, 50, 50, 50]
Shreiker = ["Shreiker", "SR", True, 10, False, 0, 0, 0, 10, 10, 10, 0, 10]
Bile_Spewer = ["Bile Spewer", "BS", True, 5, 51, True, 15, 2, 10, 2, 10, 15, 0, 15]
Stalkers = ["Stalkers", "SK", True, 15, 10, False, 0, 0, 0, 3, 5, 20, 10, 20]
Bile_Titan = ["Bile Titan", "BT", True, 100, 100, True, 75, 100, 2, 5, 5, 50, 75, 50]
bugs = [Scavenger, Pouncer, Hunter, Hive_Guard, Charger, Shreiker, Bile_Spewer, Stalkers, Bile_Titan]

Trooper = ["Trooper", "TR", False, 0, 0, True, 5, 0, 2, 5, 10, 10, 0, 10]
Comissar = ["Comissar", "CM", True, 10, 5, True, 5, 0, 3, 2, 5, 10, 0, 10]
Scout_Strider = ["Scout_Strider", "ST", True, 25, 10, True, 30, 20, 10, 15, 10, 10, 30, 10]
Beserker = ["Beserker", "BK", True, 35, 25, False, 0, 0, 0, 2, 5, 25, 10, 25]
Devistator = ["Devistator", "DV", True, 20, 5, True, 30, 5, 5, 1 , 5, 50, 25, 50]
Hulk = ["Hulk", "HK", True, 75, 10, True, 50, 100, 2, 2, 5, 30, 75, 30]
Tank = ["Tank", "TK", True, 20, 100, True, 80, 100, 10, 5, 15, 30, 100, 30]
Factory_Strider = ["Factory Strider", "FS", True, 100, 100, True, 75, 50, 5, 1, 10, 50, 150, 50]
bots = [Trooper, Comissar, Scout_Strider, Beserker, Devistator, Hulk, Tank, Factory_Strider]
Voteless = ["Voteless", "VT", True, 5, 0, False, 0, 0, 0, 5, 5, 5, 0, 5]
Watcher = ["Watcher", "WC", False, 0, 0, True, 20, 5, 2, 5, 10, 10, 5, 5, 5]
Overseer = ["Overseer", "OS", True, 50, 0, False, 0, 0, 0, 5, 7, 20, 30, 20]
Elevated_Overseer = ["Elevated Overseer", "EO", False, 0, 0, True, 20, 5, 5, 1, 5, 20, 15, 20]
Cresent_Overseer = ["Cresent Overseer", "CO", False, 0, 0, True, 50, 25, 10, 10, 3, 20, 15, 20]
Flesh_Mob = ["Flesh Mob", "FM", True, 25, 0, False, 0, 0, 0, 4, 5, 200, 0, 200]
Harvester = ["Harvester", "HV", True, 50, 25, True, 100, 50, 5, 2, 10, 25, 85, 25]
squids = [Voteless, Watcher, Overseer, Elevated_Overseer, Cresent_Overseer, Flesh_Mob, Harvester]

for bug in bugs:
    print(f"{bug[0]}, {len(bug)}")
for bot in bots:
    print(f"{bot[0]}, {len(bot)}")
for squid in squids:
    print(f"{squid[0]}, {len(squid)}")