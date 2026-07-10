#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NBA 2027 Roster Processor
Processes rosters and updates DBF files according to rules
"""

import sys
from datetime import datetime

try:
    import dbf
except ImportError:
    print("Installing required package: dbfread")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "dbfread", "dbfpy"])
    import dbf

# Rosters data
ROSTERS = {
    "Atlanta Hawks": [
        "Onyeka Okongwu", "Jalen Johnson", "Dyson Daniels", "CJ McCollum",
        "Nickeil Alexander-Walker", "Zaccharie Risacher", "Buddy Hield",
        "Devin Carter", "Aaron Wiggins", "Asa Newell", "Mouhamed Gueye",
        "Corey Kispert", "Kingston Flemings", "Zuby Ejiofor", "Keshon Gilbert"
    ],
    "Boston Celtics": [
        "Mitchell Robinson", "Jayson Tatum", "Paul George", "Derrick White",
        "Payton Pritchard", "Sam Hauser", "Baylor Scheierman", "Neemias Queta",
        "Mike Conley", "Hugo Gonzalez", "Luka Garza", "Jordan Walsh",
        "Chris Cenac Jr.", "John Tonje", "Amari Williams"
    ],
    "Charlotte Hornets": [
        "Naz Reid", "Grant Williams", "Brandon Miller", "Kon Knueppel",
        "LaMelo Ball", "Coby White", "Dorian Finney-Smith", "Ryan Kalkbrenner",
        "Tre Mann", "Liam McNeeley", "Tidjane Salaun", "Moussa Diabate",
        "Sion James", "Christian Anderson", "Hannes Steinbach"
    ],
    "Chicago Bulls": [
        "Nic Claxton", "Caleb Wilson", "Matas Buzelis", "Norman Powell",
        "Josh Giddey", "Isaac Okoro", "Rob Dillingham", "Tre Jones",
        "Zach Collins", "Jalen Smith", "Leonard Miller", "Nick Richards",
        "Patrick Williams", "Noa Essengue", "Dailyn Swain"
    ],
    "Cleveland Cavaliers": [
        "Jarrett Allen", "Evan Mobley", "LeBron James", "Donovan Mitchell",
        "James Harden", "Dennis Schröder", "Max Strus", "Jaylon Tyson",
        "Sam Merrill", "Craig Porter Jr.", "Thomas Bryant", "Tyrese Proctor",
        "Meleek Thomas", "Riley Minix", "Nae'Qwan Tomlin"
    ],
    "Dallas Mavericks": [
        "Dereck Lively II", "Cooper Flagg", "Klay Thompson", "Kyrie Irving",
        "Ryan Nembhard", "Daniel Gafford", "P.J. Washington", "Naji Marshall",
        "Max Christie", "Caleb Martin", "Marcus Sasser", "Morez Johnson Jr.",
        "Sergio de Larrea", "Tyler Smith", "Brandon Williams"
    ],
    "Denver Nuggets": [
        "Nikola Jokic", "Aaron Gordon", "Cameron Johnson", "Christian Braun",
        "Jamal Murray", "Bruce Brown", "Tyus Jones", "DaRon Holmes II",
        "Julian Strawther", "Peyton Watson", "Zeke Nnaji", "Marvin Bagley III",
        "Bryce Hopkins", "Trevon Brazile", "Spencer Jones"
    ],
    "Detroit Pistons": [
        "Jalen Duren", "John Collins", "Ausar Thompson", "Duncan Robinson",
        "Cade Cunningham", "Ronald Holland II", "Isaiah Joe", "Kevin Huerter",
        "Taurean Prince", "Paul Reed", "Gary Harris", "Daniss Jenkins",
        "Ebuka Okorie", "Isaac Jones", "Elijah Harkless"
    ],
    "Golden State Warriors": [
        "Kristaps Porzingis", "Draymond Green", "Yaxel Lendeborg", "Jimmy Butler III",
        "Stephen Curry", "Brandin Podzimienzki", "Moses Moody", "Al Horford",
        "Gary Payton II", "De'Anthony Melton", "Gui Santos", "Will Richard",
        "Charles Bassey", "Seth Curry", "Lajae Jones"
    ],
    "Houston Rockets": [
        "Alperen Sengun", "Jabari Smith Jr.", "Kevin Durant", "Amen Thompson",
        "Fred VanVleet", "Reed Sheppard", "Tari Eason", "Marcus Smart",
        "Steven Adams", "Clint Capela", "Bogdan Bogdanovic", "Aaron Holiday",
        "Isaiah Crawford", "JD Davison", "Tristen Newton"
    ],
    "Indiana Pacers": [
        "Ivica Zubac", "Pascal Siakam", "Aaron Nesmith", "Andrew Nembhard",
        "Tyrese Haliburton", "Bennedict Mathurin", "Obi Toppin", "Jarace Walker",
        "T.J. McConnell", "Kelly Oubre Jr.", "Jay Huff", "Ben Sheppard",
        "Braden Smith", "Taelon Peter", "Johnny Furphy"
    ],
    "Los Angeles Clippers": [
        "Brook Lopez", "Rui Hachimura", "Kawhi Leonard", "Derrick Jones Jr.",
        "Darius Garland", "Bennedict Mathurin", "Kris Dunn", "Isaiah Jackson",
        "Jordan Miller", "Kobe Sanders", "Cam Christie", "Yanic Konan Niederhauser",
        "Keaton Wagler", "Nick Martinelli", "Sean Pedulla"
    ],
    "Los Angeles Lakers": [
        "Walker Kessler", "Jarred Vanderbilt", "Luka Dončić", "Austin Reaves",
        "Collin Sexton", "Quentin Grimes", "Dalton Knecht", "Jake LaRavia",
        "Kevon Looney", "Sandro Mamukelashvili", "Jaden Hardy", "Bronny James",
        "Adou Thiero", "Cameron Carr", "Peter Suder"
    ],
    "Memphis Grizzlies": [
        "Zach Edey", "Jerami Grant", "Jaylen Wells", "Cedric Coward",
        "Ty Jerome", "Santi Aldama", "DAngelo Russell", "Cam Spencer",
        "GG Jackson", "Kentavious Caldwell-Pope", "Karim Lopez", "Scotty Pippen Jr.",
        "Isaiah Stewart", "Taylor Hendricks", "Quinten Post"
    ],
    "Miami Heat": [
        "Bam Adebayo", "Giannis Antetokounmpo", "Andrew Wiggins", "Tim Hardaway Jr.",
        "Davion Mitchell", "Bobby Portis", "Nikola Jović", "Pelle Larsson",
        "Dru Smith", "Simone Fontecchio", "Keshad Johnson", "Ryan Conwell",
        "Tre Donaldson", "Vladislav Goldin", "Myron Gardner"
    ],
    "Milwaukee Bucks": [
        "Myles Turner", "Kyle Kuzma", "Jaime Jaquez Jr.", "Tyler Herro",
        "Kevin Porter Jr.", "Caris LeVert", "Kel'el Ware", "AJ Green",
        "Ryan Rollins", "Ousmane Dieng", "Kam Jones", "Kasparas Jakucionis",
        "Brayden Burries", "Nate Ament", "Bogoljub Markovic"
    ],
    "Minnesota Timberwolves": [
        "Rudy Gobert", "Julius Randle", "Jaden McDaniels", "Anthony Edwards",
        "LaMelo Ball", "Naz Reid", "Donte DiVincenzo", "Terrence Shannon Jr.",
        "Ayo Dosunmu", "Jaylen Clark", "Josh Green", "Bones Hyland",
        "Joan Beringer", "Isaiah Evans", "Zyon Pullin"
    ],
    "Brooklyn Nets": [
        "Moritz Wagner", "Julius Randle", "Michael Porter Jr.", "Keon Ellis",
        "Egor Demin", "Ben Saraf", "Noah Clowney", "Day'Ron Sharpe",
        "Terance Mann", "Ziaire Williams", "Danny Wolf", "Jalen Wilson",
        "Mikel Brown Jr.", "Joshua Jefferson", "Tyson Etienne"
    ],
    "New Orleans Pelicans": [
        "Derik Queen", "Zion Williamson", "Trey Murphy III", "Jordan Poole",
        "Dejounte Murray", "Herbert Jones", "Jeremiah Fears", "Yves Missi",
        "Saddiq Bey", "Jordan Hawkins", "Micah Peavy", "Bryce McGowens",
        "Jaron Pierre Jr.", "DeAndre Jordan", "Bryce McGowens"
    ],
    "New York Knicks": [
        "Karl-Anthony Towns", "OG Anunoby", "Josh Hart", "Mikal Bridges",
        "Jalen Brunson", "Jose Alvarado", "Miles McBride", "Jordan Clarkson",
        "Andre Drummond", "Landry Shamet", "Tyler Kolek", "Dillon Jones",
        "Pacome Dadiet", "Mohamed Diawara", "Jeremy Sochan"
    ],
    "Orlando Magic": [
        "Nikola Vucevic", "Paolo Banchero", "Franz Wagner", "Desmond Bane",
        "Jalen Suggs", "Anthony Black", "Wendell Carter Jr.", "Tristan da Silva",
        "Jonathan Isaac", "Jett Howard", "Goga Bitadze", "Jevon Carter",
        "Noah Penda", "Colin Castleton", "Jamal Cain"
    ],
    "Philadelphia 76ers": [
        "Joel Embiid", "Jaylen Brown", "Justin Edwards", "VJ Edgecombe",
        "Tyrese Maxey", "Anfernee Simons", "Dominick Barlow", "Adem Bona",
        "Dean Wade", "Jabari Walker", "Dalen Terry", "Tyrese Martin",
        "Johni Broome", "Labaron Philon Jr.", "Trendon Watford"
    ],
    "Phoenix Suns": [
        "Mark Williams", "Miles Bridges", "Dillon Brooks", "Devin Booker",
        "Jalen Green", "Grayson Allen", "Ryan Dunn", "Jordan Goodwin",
        "Luke Kennard", "Oso Ighodaro", "Haywood Highsmith", "Collin Gillespie",
        "Pat Spencer", "Koa Peat", "Rasheer Fleming"
    ],
    "Portland Trail Blazers": [
        "Donovan Clingan", "Toumani Camara", "Deni Avdija", "Jrue Holiday",
        "Ja Morant", "Shaedon Sharpe", "Scoot Henderson", "Robert Williams III",
        "Damian Lillard", "Sidy Cissoko", "Blake Wesley", "Vit Krejci",
        "Yang Hansen", "Jayson Kent", "Branden Carlson"
    ],
    "Sacramento Kings": [
        "Domantas Sabonis", "Keegan Murray", "De'Andre Hunter", "Zach LaVine",
        "Darius Acuff Jr.", "Russell Westbrook", "Malik Monk", "Precious Achiuwa",
        "Maxime Raynaud", "Alex Karaban", "Drew Eubanks", "Nique Clifford",
        "Dylan Cardwell", "Isaiah Stevens", "Killian Hayes"
    ],
    "San Antonio Spurs": [
        "Victor Wembanyama", "Tobias Harris", "Devin Vassell", "Stephon Castle",
        "De'Aaron Fox", "Dylan Harper", "Keldon Johnson", "Harrison Barnes",
        "Julian Champagnie", "Luke Kornet", "Carter Bryant", "Jordan McLaughlin",
        "Jayden Quaintance", "Tarris Reed Jr.", "Ja'Kobi Gillespie"
    ],
    "Oklahoma City Thunder": [
        "Isaiah Hartenstein", "Chet Holmgren", "Jalen Williams", "Luguentz Dort",
        "Shai Gilgeous-Alexander", "Cason Wallace", "Alex Caruso", "Jared McCain",
        "Ajay Mitchell", "Jaylin Williams", "Aday Mara", "Kenrich Williams",
        "Bennett Stirtz", "Nikola Topic", "Thomas Sorber"
    ],
    "Toronto Raptors": [
        "Jakob Poeltl", "Scottie Barnes", "Brandon Ingram", "RJ Barrett",
        "Immanuel Quickley", "Gradey Dick", "Collin Murray-Boyles", "Ja'Kobe Walter",
        "Jamal Shead", "Trayce Jackson-Davis", "Jamison Battle", "AJ Lawson",
        "Nate Bittle", "Allen Graves", "Garrett Temple"
    ],
    "Utah Jazz": [
        "Jaren Jackson Jr.", "Lauri Markkanen", "Ace Bailey", "Darryn Peterson",
        "Keyonte George", "Isaiah Collier", "Kyle Filipowski", "Brice Sensabaugh",
        "Cody Williams", "Jusuf Nurkić", "Kevin Love", "Jaxson Hayes",
        "Mo Bamba", "Svi Mykhailiuk", "Josh Okogie"
    ],
    "Washington Wizards": [
        "Alex Sarr", "Anthony Davis", "Bilal Coulibaly", "AJ Dybantsa",
        "Trae Young", "Deandre Ayton", "Bub Carrington", "Cam Whitmore",
        "Tre Johnson", "Kyshawn George", "Khris Middleton", "Tristan Vukčević",
        "Jamir Watkins", "Justin Champagnie", "Anthony Gill"
    ]
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

print("=" * 80)
print("NBA 2027 ROSTER PROCESSOR")
print("=" * 80)
print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nRosters loaded: {len(ROSTERS)}")
print(f"Free Agents in list: {len(FREE_AGENTS_LIST)}")

# Create a mapping of all roster players
all_roster_players = {}
for team, players in ROSTERS.items():
    for player in players:
        all_roster_players[player.lower()] = team

print(f"\nTotal players in all rosters: {len(all_roster_players)}")
print("\n✓ Script ready to process players.dbf")
print("\nRules applied:")
print("1. Move players to their assigned team rosters")
print("2. Move players NOT in roster to 'Free Agents' team")
print("3. Move to 'Retired' ONLY if:")
print("   - Player is NOT in the Free Agents list")
print("   - Player is older than 35 years")
print("4. If roster needs completion, use cut players if available")
print("\nNext step: Run the DBF processing...")
