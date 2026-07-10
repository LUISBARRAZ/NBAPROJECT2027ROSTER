#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NBA 2027 Roster Processor for DBF
Processes players.dbf and updates team assignments, positions, and status
"""

import struct
from datetime import datetime

def get_fields(data):
    """Extract field definitions from DBF header"""
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

def load_dbf(path):
    """Load DBF file and extract structure"""
    with open(path, 'rb') as f:
        data = bytearray(f.read())
    
    header_size = struct.unpack('<H', data[8:10])[0]
    record_length = struct.unpack('<H', data[10:12])[0]
    num_records = struct.unpack('<I', data[4:8])[0]
    fields = get_fields(data)
    
    # Build field offset map
    field_offsets = {}
    off = 1
    for (name, ft, fl, fd) in fields:
        field_offsets[name] = (ft, fl, fd, off)
        off += fl
    
    return data, header_size, record_length, num_records, field_offsets

def get_field_value(data, record_start, field_offsets, field_name):
    """Get field value from a record"""
    ft, fl, fd, off = field_offsets[field_name]
    raw = data[record_start + off : record_start + off + fl]
    
    if ft == 'N':
        s = raw.replace(b'\x00', b' ').decode('latin-1').strip()
        try:
            return int(s) if s else 0
        except:
            return raw
    elif ft == 'C':
        return raw.decode('latin-1').strip()
    return raw

def set_field_value(data, record_start, field_offsets, field_name, value):
    """Set field value in a record"""
    ft, fl, fd, field_offsets_dict = field_offsets[field_name]
    
    if ft == 'C':
        s = str(value).ljust(fl).encode('latin-1')[:fl]
    else:
        s = str(value).rjust(fl).encode('latin-1')[:fl]
    
    assert len(s) == fl, f"Field {field_name}: expected {fl} bytes, got {len(s)}"
    data[record_start + field_offsets_dict : record_start + field_offsets_dict + fl] = s

# Define rosters
ROSTERS = {
    0: ["Onyeka Okongwu", "Jalen Johnson", "Dyson Daniels", "CJ McCollum",
        "Nickeil Alexander-Walker", "Zaccharie Risacher", "Buddy Hield",
        "Devin Carter", "Aaron Wiggins", "Asa Newell", "Mouhamed Gueye",
        "Corey Kispert", "Kingston Flemings", "Zuby Ejiofor", "Keshon Gilbert"],
    1: ["Mitchell Robinson", "Jayson Tatum", "Paul George", "Derrick White",
        "Payton Pritchard", "Sam Hauser", "Baylor Scheierman", "Neemias Queta",
        "Mike Conley", "Hugo Gonzalez", "Luka Garza", "Jordan Walsh",
        "Chris Cenac Jr.", "John Tonje", "Amari Williams"],
    # ... agregar todos los 30 equipos
}

FREE_AGENTS_LIST = [
    "DeMar DeRozan", "Brandon Williams", "Jonathan Kuminga", "Jonas Valanciunas",
    "Malik Beasley", "Jaden Ivey", "Ben Simmons", "Malcolm Brogdon",
    "Micah Potter", "Guerschon Yabusele", "Spencer Dinwiddie", "Cam Thomas",
    "Cole Anthony", "Jeremiah Robinson-Earl", "Dante Exum", "Cameron Payne",
    # ... etc
]

print("=" * 80)
print("NBA 2027 ROSTER DBF PROCESSOR")
print("=" * 80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load DBF
print("\n📂 Loading players.dbf...")
try:
    data, header_size, record_length, num_records, field_offsets = load_dbf('players.dbf')
    print(f"✅ DBF loaded: {num_records} records, {record_length} bytes per record")
except Exception as e:
    print(f"❌ Error loading DBF: {e}")
    exit(1)

# Process records
print("\n🔄 Processing roster assignments...")
assignments = 0
free_agents_count = 0
retired_count = 0

for i in range(num_records):
    record_start = header_size + i * record_length
    
    # Get player info
    player_name = get_field_value(data, record_start, field_offsets, 'NAME')
    first_name = get_field_value(data, record_start, field_offsets, 'FNAME')
    player_age = get_field_value(data, record_start, field_offsets, 'AGE')
    
    full_name = f"{first_name} {player_name}".strip()
    
    # Check if player is in any roster
    assigned = False
    for team_id, roster_players in ROSTERS.items():
        if any(p.lower() in full_name.lower() for p in roster_players):
            set_field_value(data, record_start, field_offsets, 'TEAM', team_id)
            assignments += 1
            assigned = True
            break
    
    # If not assigned to team, check if Free Agent
    if not assigned:
        if any(p.lower() in full_name.lower() for p in FREE_AGENTS_LIST):
            set_field_value(data, record_start, field_offsets, 'TEAM', 50)  # Free Agents
            free_agents_count += 1
        elif player_age and int(player_age) > 35:
            # Move to Retired if > 35 AND not in Free Agents
            set_field_value(data, record_start, field_offsets, 'TEAM', 99)  # Retired
            retired_count += 1

print(f"✅ Team assignments: {assignments}")
print(f"✅ Free Agents assigned: {free_agents_count}")
print(f"✅ Retired assigned: {retired_count}")

# Save updated DBF
output_file = 'players_UPDATED_2027.dbf'
print(f"\n💾 Saving to {output_file}...")
try:
    with open(output_file, 'wb') as f:
        f.write(data)
    print(f"✅ Saved successfully: {len(data)} bytes")
except Exception as e:
    print(f"❌ Error saving: {e}")
    exit(1)

print("\n" + "=" * 80)
print("✅ PROCESS COMPLETED SUCCESSFULLY")
print("=" * 80)
print(f"\n📊 Summary:")
print(f"   • Total records processed: {num_records}")
print(f"   • Team assignments: {assignments}")
print(f"   • Free Agents: {free_agents_count}")
print(f"   • Retired: {retired_count}")
print(f"\n📁 Output file: {output_file}")
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
