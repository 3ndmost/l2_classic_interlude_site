# Systems scorecard

The overall progress on the site is worked out from this table. Each Interlude system has a size (3 large, 2 medium,
1 small: roughly how much of the game it is) and a state:

- tested: played on the Classic client and accepted (1.0)
- mostly: tested, with known open points (0.85)
- partly: some parts tested, others not (0.6)
- untested: the Classic code path exists, nobody has tried it in game yet (0.4)
- unchecked: not looked at for the Classic client yet (0.2)

Progress = sum(size x state value) / sum(size). Edit a state when a test result comes in; the next build uses it.
Gameplay rules themselves are aCis's (the Interlude reference) and are not scored here: this measures whether each
system works through the Classic client.

| System | Size | State | Note |
|---|---|---|---|
| Login, server list, character select and creation | 3 | tested | Wrong password and banned account fixed 2026-11-13 |
| World entry, visibility, targeting | 3 | tested | |
| Movement, keyboard walking, camera | 3 | tested | WASD and camera zoom tested 2026-11-13 |
| Combat, death, resurrection | 3 | tested | |
| Skills: learning, use, toggles, enchant | 3 | mostly | Some skills fail from the Skill window (names awaited) |
| Damage numbers, buffs and effects | 2 | mostly | Damage over time numbers not confirmed |
| Inventory, equipment, enchanting, crystals | 3 | tested | |
| Shops, multisell, GM shop | 2 | tested | |
| Trade, private stores, manufacture | 2 | tested | |
| Warehouses and freight | 2 | mostly | Castle warehouse not tried |
| Crafting | 1 | tested | |
| Augmentation and dyes | 2 | tested | |
| Party and party matching | 2 | tested | |
| Chat, whispers, friends, block list, mail | 2 | tested | |
| Clan, alliance, clan wars, crests | 3 | mostly | Clan war surrender not tried |
| Castle sieges | 3 | tested | Tested 2026-10-24 |
| Clan halls: sieges, auctions, functions | 2 | partly | Auctions and decorations tested; clan hall sieges not |
| Manor | 2 | partly | Code mapped; the 06:00 charge and per-castle lists await a test |
| Command channel | 1 | partly | Loot rule not tried |
| Olympiad and heroes | 3 | partly | Matches and hero list tested; tower observation and slash commands not |
| Seven Signs, Festival of Darkness, catacombs | 3 | untested | Record window, sky and zone names done; the festival never played |
| Dimensional Rift and Four Sepulchers | 2 | unchecked | |
| Raid and grand bosses, raid points | 2 | untested | The client has no raid point window |
| Quests (343 on the server) | 3 | partly | Journal, markers and a few quests tested (quest 127 end to end, 2026-11-18); most quests never played on 110 |
| Tutorial, newbie guide, daily missions | 2 | tested | |
| Pets and summons | 3 | mostly | Fixed and tested 2026-11-13 |
| Mounts: strider and wyvern | 1 | mostly | Wyvern not tried |
| Boats, swimming, doors | 2 | tested | |
| Fishing | 2 | tested | |
| PvP, karma, duels | 2 | tested | Duels tested 2026-10-31 |
| Cursed weapons | 1 | mostly | Map location not shown |
| Sub-class, noblesse, class change | 2 | partly | Class change tested; sub-class and noblesse quests not played |
| Teleports, gatekeepers, buffers, herbs | 2 | mostly | Herb level range awaits a test |
| Recommendations, petitions, bot reports, anti-bot check | 1 | tested | |
| World Info, maps, region info | 2 | tested | |
| Community board, GM and admin tools | 2 | tested | |
| Events | 1 | tested | Change of Heart tested 2026-11-14 |
| Lottery, Monster Race, wedding | 1 | unchecked | |
| Cinematics | 1 | tested | Quest 127's movie with replay, tested 2026-11-18 |
