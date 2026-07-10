# NBA 2027 Roster DBF Update - Instructions

## Overview
This document provides the step-by-step instructions for updating the players.dbf file with the new 2027 roster assignments.

## Rules Applied

### Rule 1: Team Assignment
Each player listed in ROSTER_ASSIGNMENTS_2027.csv must be assigned to their designated team based on position (C, PF, SF, SG, PG, or BENCH).

### Rule 2: Free Agents Assignment
Players not in any of the 30 team rosters must be moved to the "Free Agents" team entry.

### Rule 3: Retired Assignment
Players are moved to "Retired" status ONLY if BOTH conditions are met:
- Player is NOT in the Free Agents list (see ROSTER_ASSIGNMENTS_2027.csv)
- Player age is greater than 35 years old

### Rule 4: Roster Completion
If any team roster has fewer than 15 active players:
- Check the "Cortados" (cut players) list provided for that team
- If cut players exist in the DBF, add them to the roster to reach 15 players
- This only applies to teams with incomplete rosters

## Cut Players Reference

### Atlanta Hawks Cortados
- Tony Bradley
- RayJ Dennis
- Christian Koloko
- Jock Landale
- Gabe Vincent
- Keaton Wallace

### Boston Celtics Cortados
- Ron Harper Jr.
- Dillon Mitchell

### Charlotte Hornets Cortados
- Pat Connaughton
- PJ Hall
- Grayson Allen
- Royce O'Neale
- Xavier Tillman

[Continue for all teams...]

## DBF Fields to Update

- `TEAM_NAME`: Updated team assignment
- `TEAM_ID`: Numeric ID for the team
- `POSITION`: Player's position (C, PF, SF, SG, PG)
- `STATUS`: Status field (Active, Free Agent, Retired)

## Verification Steps

1. ✓ All 30 teams have exactly 15 active players
2. ✓ Free Agents section contains all unassigned players
3. ✓ Retired section contains only players >35 years old NOT in Free Agents
4. ✓ No duplicate players across teams
5. ✓ All positions are correctly assigned (C, PF, SF, SG, PG)

## Timeline

- Database updated: 2026-07-10
- Season start: 2026-2027
- Total rosters: 30 NBA teams + Free Agents + Retired
