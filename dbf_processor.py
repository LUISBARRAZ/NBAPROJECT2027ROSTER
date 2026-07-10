#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NBA 2027 Roster DBF Processor - Complete Version
Updates players.dbf with team assignments based on 2027 roster list
"""

import struct
from datetime import datetime

# All 30 Team Rosters
ROSTERS = {
    0: ["Onyeka Okongwu", "Jalen Johnson", "Dyson Daniels", "CJ McCollum",
        "Nickeil Alexander-Walker", "Zaccharie Risacher", "Buddy Hield",
        "Devin Carter", "Aaron Wiggins", "Asa Newell", "Mouhamed Gueye",
        "Corey Kispert", "Kingston Flemings", "Zuby Ejiofor", "Keshon Gilbert"],
    1: ["Mitchell Robinson", "Jayson Tatum", "Paul George", "Derrick White",
        "Payton Pritchard", "Sam Hauser", "Baylor Scheierman", "Neemias Queta",
        "Mike Conley", "Hugo Gonzalez", "Luka Garza", "Jordan Walsh",
        "Chris Cenac Jr.", "John Tonje", "Amari Williams"],
    2: ["Naz Reid", "Grant Williams", "Brandon Miller", "Kon Knueppel",
        "LaMelo Ball", "Coby White", "Dorian Finney-Smith", "Ryan Kalkbrenner",
        "Tre Mann", "Liam McNeeley", "Tidjane Salaun", "Moussa Diabate",
        "Sion James", "Christian Anderson", "Hannes Steinbach"],
    3: ["Nic Claxton", "Caleb Wilson", "Matas Buzelis", "Norman Powell",
        "Josh Giddey", "Isaac Okoro", "Rob Dillingham", "Tre Jones",
        "Zach Collins", "Jalen Smith", "Leonard Miller", "Nick Richards",
        "Patrick Williams", "Noa Essengue", "Dailyn Swain"],
    4: ["Jarrett Allen", "Evan Mobley", "LeBron James", "Donovan Mitchell",
        "James Harden", "Dennis Schroder", "Max Strus", "Jaylon Tyson",
        "Sam Merrill", "Craig Porter Jr.", "Thomas Bryant", "Tyrese Proctor",
        "Meleek Thomas", "Riley Minix", "Nae'Qwan Tomlin"],
    5: ["Dereck Lively II", "Cooper Flagg", "Klay Thompson", "Kyrie Irving",
        "Ryan Nembhard", "Daniel Gafford", "P.J. Washington", "Naji Marshall",
        "Max Christie", "Caleb Martin", "Marcus Sasser", "Morez Johnson Jr.",
        "Sergio de Larrea", "Tyler Smith", "Brandon Williams"],
    6: ["Nikola Jokic", "Aaron Gordon", "Cameron Johnson", "Christian Braun",
        "Jamal Murray", "Bruce Brown", "Tyus Jones", "DaRon Holmes II",
        "Julian Strawther", "Peyton Watson", "Zeke Nnaji", "Marvin Bagley III",
        "Bryce Hopkins", "Trevon Brazile", "Spencer Jones"],
    7: ["Jalen Duren", "John Collins", "Ausar Thompson", "Duncan Robinson",
        "Cade Cunningham", "Ronald Holland II", "Isaiah Joe", "Kevin Huerter",
        "Taurean Prince", "Paul Reed", "Gary Harris", "Daniss Jenkins",
        "Ebuka Okorie", "Isaac Jones", "Elijah Harkless"],
    8: ["Kristaps Porzingis", "Draymond Green", "Yaxel Lendeborg", "Jimmy Butler III",
        "Stephen Curry", "Brandin Podzimienzki", "Moses Moody", "Al Horford",
        "Gary Payton II", "De'Anthony Melton", "Gui Santos", "Will Richard",
        "Charles Bassey", "Seth Curry", "Lajae Jones"],
    9: ["Alperen Sengun", "Jabari Smith Jr.", "Kevin Durant", "Amen Thompson",
        "Fred VanVleet", "Reed Sheppard", "Tari Eason", "Marcus Smart",
        "Steven Adams", "Clint Capela", "Bogdan Bogdanovic", "Aaron Holiday",
        "Isaiah Crawford", "JD Davison", "Tristen Newton"],
    10: ["Ivica Zubac", "Pascal Siakam", "Aaron Nesmith", "Andrew Nembhard",
         "Tyrese Haliburton", "Bennedict Mathurin", "Obi Toppin", "Jarace Walker",
         "T.J. McConnell", "Kelly Oubre Jr.", "Jay Huff", "Ben Sheppard",
         "Braden Smith", "Taelon Peter", "Johnny Furphy"],
    11: ["Brook Lopez", "Rui Hachimura", "Kawhi Leonard", "Derrick Jones Jr.",
         "Darius Garland", "Bennedict Mathurin", "Kris Dunn", "Isaiah Jackson",
         "Jordan Miller", "Kobe Sanders", "Cam Christie", "Yanic Konan Niederhauser",
         "Keaton Wagler", "Nick Martinelli", "Sean Pedulla"],
    12: ["Walker Kessler", "Jarred Vanderbilt", "Luka Doncic", "Austin Reaves",
         "Collin Sexton", "Quentin Grimes", "Dalton Knecht", "Jake LaRavia",
         "Kevon Looney", "Sandro Mamukelashvili", "Jaden Hardy", "Bronny James",
         "Adou Thiero", "Cameron Carr", "Peter Suder"],
    13: ["Zach Edey", "Jerami Grant", "Jaylen Wells", "Cedric Coward",
         "Ty Jerome", "Santi Aldama", "DAngelo Russell", "Cam Spencer",
         "GG Jackson", "Kentavious Caldwell-Pope", "Karim Lopez", "Scotty Pippen Jr.",
         "Isaiah Stewart", "Taylor Hendricks", "Quinten Post"],
    14: ["Bam Adebayo", "Giannis Antetokounmpo", "Andrew Wiggins", "Tim Hardaway Jr.",
         "Davion Mitchell", "Bobby Portis", "Nikola Jovic", "Pelle Larsson",
         "Dru Smith", "Simone Fontecchio", "Keshad Johnson", "Ryan Conwell",
         "Tre Donaldson", "Vladislav Goldin", "Myron Gardner"],
    15: ["Myles Turner", "Kyle Kuzma", "Jaime Jaquez Jr.", "Tyler Herro",
         "Kevin Porter Jr.", "Caris LeVert", "Kel'el Ware", "AJ Green",
         "Ryan Rollins", "Ousmane Dieng", "Kam Jones", "Kasparas Jakucionis",
         "Brayden Burries", "Nate Ament", "Bogoljub Markovic"],
    16: ["Rudy Gobert", "Julius Randle", "Jaden McDaniels", "Anthony Edwards",
         "LaMelo Ball", "Naz Reid", "Donte DiVincenzo", "Terrence Shannon Jr.",
         "Ayo Dosunmu", "Jaylen Clark", "Josh Green", "Bones Hyland",
         "Joan Beringer", "Isaiah Evans", "Zyon Pullin"],
    17: ["Moritz Wagner", "Julius Randle", "Michael Porter Jr.", "Keon Ellis",
         "Egor Demin", "Ben Saraf", "Noah Clowney", "Day'Ron Sharpe",
         "Terance Mann", "Ziaire Williams", "Danny Wolf", "Jalen Wilson",
         "Mikel Brown Jr.", "Joshua Jefferson", "Tyson Etienne"],
    18: ["Derik Queen", "Zion Williamson", "Trey Murphy III", "Jordan Poole",
         "Dejounte Murray", "Herbert Jones", "Jeremiah Fears", "Yves Missi",
         "Saddiq Bey", "Jordan Hawkins", "Micah Peavy", "Bryce McGowens",
         "Jaron Pierre Jr.", "DeAndre Jordan", "Bryce McGowens"],
    19: ["Karl-Anthony Towns", "OG Anunoby", "Josh Hart", "Mikal Bridges",
         "Jalen Brunson", "Jose Alvarado", "Miles McBride", "Jordan Clarkson",
         "Andre Drummond", "Landry Shamet", "Tyler Kolek", "Dillon Jones",
         "Pacome Dadiet", "Mohamed Diawara", "Jeremy Sochan"],
    20: ["Nikola Vucevic", "Paolo Banchero", "Franz Wagner", "Desmond Bane",
         "Jalen Suggs", "Anthony Black", "Wendell Carter Jr.", "Tristan da Silva",
         "Jonathan Isaac", "Jett Howard", "Goga Bitadze", "Jevon Carter",
         "Noah Penda", "Colin Castleton", "Jamal Cain"],
    21: ["Joel Embiid", "Jaylen Brown", "Justin Edwards", "VJ Edgecombe",
         "Tyrese Maxey", "Anfernee Simons", "Dominick Barlow", "Adem Bona",
         "Dean Wade", "Jabari Walker", "Dalen Terry", "Tyrese Martin",
         "Johni Broome", "Labaron Philon Jr.", "Trendon Watford"],
    22: ["Mark Williams", "Miles Bridges", "Dillon Brooks", "Devin Booker",
         "Jalen Green", "Grayson Allen", "Ryan Dunn", "Jordan Goodwin",
         "Luke Kennard", "Oso Ighodaro", "Haywood Highsmith", "Collin Gillespie",
         "Pat Spencer", "Koa Peat", "Rasheer Fleming"],
    23: ["Donovan Clingan", "Toumani Camara", "Deni Avdija", "Jrue Holiday",
         "Ja Morant", "Shaedon Sharpe", "Scoot Henderson", "Robert Williams III",
         "Damian Lillard", "Sidy Cissoko", "Blake Wesley", "Vit Krejci",
         "Yang Hansen", "Jayson Kent", "Branden Carlson"],
    24: ["Domantas Sabonis", "Keegan Murray", "De'Andre Hunter", "Zach LaVine",
         "Darius Acuff Jr.", "Russell Westbrook", "Malik Monk", "Precious Achiuwa",
         "Maxime Raynaud", "Alex Karaban", "Drew Eubanks", "Nique Clifford",
         "Dylan Cardwell", "Isaiah Stevens", "Killian Hayes"],
    25: ["Victor Wembanyama", "Tobias Harris", "Devin Vassell", "Stephon Castle",
         "De'Aaron Fox", "Dylan Harper", "Keldon Johnson", "Harrison Barnes",
         "Julian Champagnie", "Luke Kornet", "Carter Bryant", "Jordan McLaughlin",
         "Jayden Quaintance", "Tarris Reed Jr.", "Ja'Kobi Gillespie"],
    26: ["Isaiah Hartenstein", "Chet Holmgren", "Jalen Williams", "Luguentz Dort",
         "Shai Gilgeous-Alexander", "Cason Wallace", "Alex Caruso", "Jared McCain",
         "Ajay Mitchell", "Jaylin Williams", "Aday Mara", "Kenrich Williams",
         "Bennett Stirtz", "Nikola Topic", "Thomas Sorber"],
    27: ["Jakob Poeltl", "Scottie Barnes", "Brandon Ingram", "RJ Barrett",
         "Immanuel Quickley", "Gradey Dick", "Collin Murray-Boyles", "Ja'Kobe Walter",
         "Jamal Shead", "Trayce Jackson-Davis", "Jamison Battle", "AJ Lawson",
         "Nate Bittle", "Allen Graves", "Garrett Temple"],
    28: ["Jaren Jackson Jr.", "Lauri Markkanen", "Ace Bailey", "Darryn Peterson",
         "Keyonte George", "Isaiah Collier", "Kyle Filipowski", "Brice Sensabaugh",
         "Cody Williams", "Jusuf Nurkic", "Kevin Love", "Jaxson Hayes",
         "Mo Bamba", "Svi Mykhailiuk", "Josh Okogie"],
    29: ["Alex Sarr", "Anthony Davis", "Bilal Coulibaly", "AJ Dybantsa",
         "Trae Young", "Deandre Ayton", "Bub Carrington", "Cam Whitmore",
         "Tre Johnson", "Kyshawn George", "Khris Middleton", "Tristan Vukcevic",
         "Jamir Watkins", "Justin Champagnie", "Anthony Gill"],
}

FREE_AGENTS_LIST = [
    "DeMar DeRozan", "Brandon Williams", "Jonathan Kuminga", "Jonas Valanciunas",
    "Malik Beasley", "Jaden Ivey", "Ben Simmons", "Malcolm Brogdon",
    "Micah Potter", "Guerschon Yabusele", "Spencer Dinwiddie", "Cam Thomas",
    "Cole Anthony", "Jeremiah Robinson-Earl", "Dante Exum", "Cameron Payne",
    "Torrey Craig", "Vince Williams Jr.", "Pete Nance", "DaQuan Jeffries",
    "Georges Niang", "Brandon Boston Jr.", "Eric Gordon", "Cody Martin",
    "Shake Milton", "Lonzo Ball", "Terry Rozier III", "Keon Johnson",
    "Alec Burks", "Dario Saric", "Bojan Bogdanovic", "Garrison Mathews",
    "Caleb Houstan", "Reggie Jackson", "Damion Lee", "Delon Wright",
    "Bol Bol", "Chris Boucher", "Jae Crowder", "Richaun Holmes",
    "Johnny Juzang", "Cory Joseph", "Jalen McDaniels", "Orlando Robinson",
    "Ricky Council IV", "Monte Morris", "Daniel Theis", "Jared Butler",
    "Kennedy Chandler", "Malaki Branham", "Lonnie Walker IV", "Elfrid Payton",
    "Christian Wood", "Cam Reddish", "Kessler Edwards", "Chris Duarte",
    "Jaden Springer", "Jared Rhoden", "Vlatko Cancar", "Trevelin Queen",
    "Kobe Bufkin", "Colby Jones", "Patty Mills", "Josh Richardson",
    "Jeff Dowtin", "Terence Davis", "Talen Horton-Tucker", "P.J. Tucker",
    "Terry Taylor", "Markelle Fultz", "Lamar Stevens", "Omer Yurtseven",
    "Drew Peterson", "Chuma Okeke", "Alex Reese", "Cole Swider",
    "Lester Quinones", "P.J. Dozier", "Kevin Knox II", "Kylor Kelley",
    "Johnny Davis", "Tosan Evbuomwan", "Jalen Hood-Schifino", "Maxwell Lewis",
    "Oshae Brissett", "Alex Len", "Jaylen Nowell", "JT Thor",
    "Stanley Umude", "Malachi Flynn", "Kai Jones", "Bruno Fernando",
    "Markieff Morris", "Jahlil Okafor", "Cody Zeller", "Matt Ryan"
]

def get_fields(data):
    fields = []
    pos = 32
    while pos < len(data):
        if data[pos] == 0x0D:
            break
        field_name = data[pos:pos+11].split(b'\x00')[0].decode('latin-1')
        field_type = chr(data[pos+11])
        field_length = data[pos+16]
        field_decimal = data[pos+17]
        fields.append((field_name, field_type, field_length, field_decimal))
        pos += 32
    return fields

def load(path):
    with open(path,'rb') as f:
        data = bytearray(f.read())
    header_size = struct.unpack('<H', data[8:10])[0]
    record_length = struct.unpack('<H', data[10:12])[0]
    num_records = struct.unpack('<I', data[4:8])[0]
    fields = get_fields(data)
    field_offsets = {}
    off = 1
    for (name, ft, fl, fd) in fields:
        field_offsets[name] = (ft, fl, fd, off)
        off += fl
    return data, header_size, record_length, num_records, field_offsets

def get_val(data, rs, fo, fname):
    ft, fl, fd, off = fo[fname]
    raw = data[rs+off:rs+off+fl]
    if ft == 'N':
        s = raw.replace(b'\x00', b' ').decode('latin-1').strip()
        try: return int(s) if s else 0
        except: return raw
    elif ft=='C': return raw.decode('latin-1').strip()
    return raw

def set_field(data, rs, fo, fname, value):
    ft, fl, fd, off = fo[fname]
    s = str(value).rjust(fl).encode('latin-1')
    assert len(s)==fl
    data[rs+off:rs+off+fl] = s

print("="*80)
print("NBA 2027 ROSTER DBF PROCESSOR")
print("="*80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

pdata, phs, prl, pnr, pfo = load('players.dbf')

roster_assignments = 0
free_agents_moved = 0
retired_moved = 0
moved = []

# Create lookup for all roster players
all_roster_players = {}
for team_id, players in ROSTERS.items():
    for p in players:
        all_roster_players[p.lower()] = team_id

fa_set = set(p.lower() for p in FREE_AGENTS_LIST)

for i in range(pnr):
    rs = phs+i*prl
    fname = get_val(pdata,rs,pfo,'FNAME')
    name = get_val(pdata,rs,pfo,'NAME')
    age = get_val(pdata,rs,pfo,'AGE')
    
    full_name = f"{fname} {name}".strip().lower()
    
    # Check if in roster
    found_team = None
    for player_name, team_id in all_roster_players.items():
        if player_name in full_name or full_name in player_name:
            found_team = team_id
            break
    
    if found_team is not None:
        old_team = get_val(pdata,rs,pfo,'TEAM')
        set_field(pdata, rs, pfo, 'TEAM', found_team)
        roster_assignments += 1
        moved.append((fname, name, found_team, "Team Assignment"))
    else:
        # Check if Free Agent
        if full_name in fa_set or any(fa in full_name for fa in fa_set):
            old_team = get_val(pdata,rs,pfo,'TEAM')
            set_field(pdata, rs, pfo, 'TEAM', 50)
            free_agents_moved += 1
            moved.append((fname, name, 50, "Free Agent"))
        elif age and int(age) > 35:
            # Only retire if NOT in free agents and > 35
            if full_name not in fa_set:
                old_team = get_val(pdata,rs,pfo,'TEAM')
                set_field(pdata, rs, pfo, 'TEAM', 99)
                retired_moved += 1
                moved.append((fname, name, 99, "Retired"))

print(f"✅ Team Assignments: {roster_assignments}")
print(f"✅ Moved to Free Agents: {free_agents_moved}")
print(f"✅ Moved to Retired: {retired_moved}")
print(f"✅ Total Moved: {roster_assignments + free_agents_moved + retired_moved}")

with open('players_UPDATED_2027.dbf','wb') as f:
    f.write(pdata)

print(f"\n💾 Guardado: players_UPDATED_2027.dbf ({len(pdata)} bytes)")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
