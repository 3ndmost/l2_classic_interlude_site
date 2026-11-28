# Daily highlights

A day written here replaces the automatic picks on the Highlights tab. One "## yyyy-mm-dd" heading per day, then one
line per highlight:

    - [Area] Title | Description | commit commit ... | shots: 2026-11-13 215535, 2026-11-14 200038

The area shows its icon (areas as in build.py AREAS: Olympiad, Pets & summons, Events, Login & servers, GM tools,
Camera & movement, Combat & skills, Items & inventory, Quests & tutorial, Clan & siege, "Chat, mail & friends",
Maps & zones, Client UI, Other). The commits (their first characters are enough) become "More in the change log" links. The shots are
Windows screenshots (Pictures/Screenshots, "Screenshot <date> <time>.png"), copied small into docs/shots: check each
one for private details before it goes on the public page.

## 2026-11-28
- [GM tools] Live monster respawn speed | The dashboard's Overview can make ordinary monsters respawn 2, 5 or 10 times faster, live and kept across restarts; raid and grand bosses keep their own times. | 0a82ed60
- [GM tools] Adventurer bots test the quests | 40 % of the adventurer bots now play the server's quests through as a player does: they talk to the quest NPCs through the same links a player clicks, hunt the quest's monsters and collect the rewards, showing a green "Questing" title and saying their quest and stage in the chat. A new Quests tab on the dashboard lists every quest taken, each bot's steps with a green tick per step passed, and any problem with the full picture of when it happened. In the first five minutes of the latest test, 275 quest runs, 84 quests finished and 188 steps passed. | 826871d6 20e1a836 6f3f56dc 7fa1f508

## 2026-11-27
- [GM tools] Test bots from the dashboard | A new Bots tab spawns groups of test characters (no game clients) from presets: class, level, gear, skills, buffs, clan and alliance, a grey BOT title and realistic names, at any spot of its own map, up to a live maximum of 2000. Groups are deleted with a click, the server's lag, CPU and memory show beside them, and the Memory page measures what the bots take. | 9fb347ec 82cba760 2079e2ba | shots: 2026-11-27 141950
- [GM tools] Every GM tracked from login | GMs go on the dashboard's tracking list by themselves at each login and stay there; their movements go only when cleared or saved and deleted by hand. The tracking panel lists GMs, characters and saved sessions apart, each foldable, and the history can show one point in ten. | 72f815c4 2420b482 6ad611c1 cbadf4fc
- [GM tools] GMs asked before entering a switched-off place | A GM teleporting into Fantasy Isle or the Underground Coliseum while it is switched off gets a window saying the place has no ground loaded, with Teleport! and Cancel; either way the teleport page comes back. | 41c73728 b0efd61e bf16e9d3
- [GM tools] Dashboard map: area selection and movement tracking | Alt + drag selects any area of the map and lists its characters and NPCs, each line opening to their full details; over a crowded spot the map zooms 8 times closer. Characters put on the Tracking list have every movement stored with the time and place, teleports, logins, logouts and deaths included, shown as a list and as a line on the map, and kept as saved sessions. | 15ffe530 7c0b0cf7 fe2fb477 | shots: 2026-11-27 112049, 2026-11-27 112739
- [Maps & zones] Fantasy Isle closed at sea when switched off | With Fantasy Isle switched off (to save the server's memory), players stop at an invisible wall far out at sea, the island still in sight; switched on, the wall is gone. | 5cc5d42c
- [Maps & zones] Floor maps with their own pictures | The floor maps of the catacombs, necropolises, Forge of the Gods, Imperial Tomb, Heine, Goddard, Rune and Schuttgart, the Underground Coliseum and the Provisional Clan Halls now each have their own picture, and the fortress map slots they used to borrow hold their stock pictures again. | 822040f ad75706
- [Client UI] NPCs on the Map window | Many NPCs had no dot on the Map unless targeted: Classic hides the NPCs it does not use itself (Hasha, the Dimensional Rift's NPCs, guards, castle staff, many monsters). About 2300 of them now show (grey dots, gatekeeper and warehouse icons, red monster dots); raid bosses and their minions, chests and objects stay hidden as in Classic. | d3c8b5f
- [Maps & zones] Dimensional Rift map | The Map window showed nothing inside the Dimensional Rift: no client has a map of it. It now shows the Rift's rooms, cut from a top-down picture whose layout matches our client's. | af19bbe
- [GM tools] Dashboard map: NPC panel | A click on an NPC opens a panel like the player one: name, title, level, type, HP or dead, NPC and object id, location, map square and place, with Locate and Track. | d341f996
- [GM tools] GM speed 6 and saved GM switches | GMs get a sixth GM speed, twice speed 5, with its buff icon and //gmspeed 6; a GM still logs in at speed 5. The Admin tab's on/off pairs (fall damage, weight limit, world chat, captcha) are now single switches that show their state and keep it after logging out and after a restart. | dad19d4e 23575ccc 3bb907a6 bed9882
- [Olympiad] Every colosseum visitable | The GM teleport page lists the Olympiad's real arenas, plus the Classic map's four colosseum styles (redesigned, Hero's Trail, redesigned underground and the Classic colosseum). | 92e35d7c 01978ad4
- [Maps & zones] Classic places at a click | GM Teleport > Other Location > Classic Locations gathers the places only the Classic map has; the game server's memory is trimmed by loading geodata only where needed, and a dashboard Memory page shows where the RAM goes. | 70ce0163 8ae478d0 261b3f75 b3e5ab45
- [Client UI] Random loading and start-up pictures | Each load shows one of 27 loading pictures, and the start-up screen one of the 5 alternative Classic pictures. | bb52d57 af4d62c
- [Maps & zones] Provisional Clan Hall titles | Entering a hall shows its own name on one line, e.g. "Provisional Clan Hall - Ellia 2". | 1352ccb 014b1de0
- [Maps & zones] Fantasy Isle's beaches open | Players ran in place at the island's shore: the Classic map rings Fantasy Isle with 13 invisible walls, from just above the sea floor up into the sky. They are gone, so the beaches and the sea can be reached from the golf course and the rest of the island; rocks and buildings still block as before, and the Underground Coliseum below is untouched. | a4c0cd0
- [GM tools] Dashboard map: territory hover switch | A button on the dashboard map turns the territory highlight on mouse-over off and on; a click still keeps a territory selected, and the browser remembers the choice. | 6585e0ef

## 2026-11-26
- [Maps & zones] A Scroll of Escape keeps you in your Provisional Clan Hall | Each of the nine Provisional Clan Halls (Orchid, Ellia and Laurell 1 to 3) is now an area of its own, and a Scroll of Escape to the nearest town used inside one brings you back to that hall's arrival spot; scrolls to a named town, castle or clan hall work as before. | 014b1de0
- [GM tools] Server dashboard: a live map for GMs | The dashboard map now shows which geodata map squares the server has loaded and the memory each takes, over a sharper Interlude world map with Fantasy Isle drawn in. A click keeps a territory selected; a click on a player opens their panel (place, map square, race, class, clan, time online) with Locate and Track, which keeps the map on them as they move; Ctrl+click gives the world coordinates of any spot. | b2962966 1bdaa466 e2455423 625f3332 962c7c6a | shots: 2026-11-26 224624, 2026-11-26 224647
- [Maps & zones] Fantasy Isle, Underground Coliseum and Provisional Clan Halls named | These three places read "Neutral Waterways" on the Classic client: its place-name map leaves their map squares blank. The Classic 2.1 client draws them in a file our client lacks; its outlines are copied in and the places now carry their names, in game and in the server's reports. | 2a38e42 49d8d4d4 | shots: 2026-11-26 163816, 2026-11-26 163828, 2026-11-26 163803

## 2026-11-25
- [Maps & zones] Goddard's holy room altars | The Altar of Fire and the Altar of Water floated in Goddard Castle's holy room: Classic's map asked for a pedestal no client has. The pedestals are back, lit like the room, and both altars now stand centred on them; //npcdraw lets a GM place where the Classic client draws an NPC. | c3e2742 10b1d41 7835f9c dec4e5c4 420194c5 8e1621a5 | shots: 2026-11-25 202016
- [Maps & zones] Rune library entrance | A remade Classic bookcase stood shifted and floating in the Rune library's doorway; Rune town is drawn with Interlude's models again and the bookcase stands centred on the floor. | e1948e9 cde696a
- [Maps & zones] Primeval Isle rocks, Dragon Valley bridges, Mithril Mines | Classic's remakes of these models did not fit the Interlude maps (streaked rocks, sunken bridges, broken mine walls); they use Interlude's models and textures now. | 2173a3e e1948e9 6c151dd 74c67eb
- [Maps & zones] Fantasy Isle and the provisional clan halls walkable | The Classic client draws 32 map squares Interlude never had (Fantasy Isle, the Orchid, Ellia and Laurell provisional clan halls...); the server had no ground for them and nobody could move there. Their geodata now comes from a Classic geodata pack, matched against the client maps. | 7f2df1af
- [Maps & zones] Devastated Castle named | Most of Devastated Castle read Fields of Massacre on the Classic client; the whole castle, as the server outlines it, now reads Devastated Castle. | 983073d 73cea863
- [Maps & zones] No more "Frontier" | The Classic client named 21 places "Frontier" (Goddard Castle, the Valley of Saints, Wall of Argos, Ketra Orc Outpost, Hot Springs, Rune Harbor...); they now carry their Interlude names. | 14553d1 95ff0c38
- [GM tools] GMs enter hidden and fast | A GM now logs in hidden with GM speed 5, with a message for each; on the Classic client GMs were never set up at login (no hide, no GM list, no bot report notice), which is fixed too. | 6315878a 19c609e8

## 2026-11-24
- [Maps & zones] Monster Arena on Classic | The Classic client draws a walled Monster Arena next to the Dion race track; the server now has its floor, walls and stands, the arena combat zone covers its floor, and two Arena Managers take players in and out (free), with new HP Recovery beside CP Recovery. | 2b20bd02 bf677937 819415b9
- [Events] Monster Race runners race for real | On the Classic client all eight runners ran side by side. Each runner now gets its own pace, the client runs it at that speed, and the field spreads out smoothly with the announced winner first. | 94575851 5039ad06 a94d5f21 56e7e38
- [Events] Monster Race GM window | //monrace shows the race, its lanes, bets and odds, and starts or ends the ticket sales and the race by hand. | d40c7e66 4b93f9bf
- [GM tools] Admin tab in groups | The Admin tab of Server Management lists its tools in eight groups (players, messages, security, events, NPCs, your character, world and geodata, tests). | 99bdd1c3
- [Client UI] 48 macros | The Classic Macro window holds 48 macros; the server allowed only 24 and now allows 48. | 64c982d3 0956c5e

## 2026-11-19
- [Events] Lottery numbers show on Classic | The Lottery Ticket Seller's number grid was empty on the Classic client; it now shows Interlude's original parchment tiles 1-20. | 7c8bcb1e 59c81fe5
- [GM tools] Server Management opens on Admin | //manage now opens on the Admin tab, where the GM tools are. | 86fa713c

## 2026-11-18
- [Quests & tutorial] The Kamael movie of quest 127 | Rodemai's story now plays full screen as on Interlude, with its original music, and players can watch it again at step 8 before moving on. | cc901ef1 28c19a67 8aecbc2 c40c5df
- [Client UI] Movies play on a Classic server | The client never loaded its movie table on a Classic server; now every client movie plays, and only GMs can stop one (Esc). | c13c3f2 28c19a67
- [GM tools] //playmovie and quest reset | GMs can play any client movie and reset a finished quest from the Admin tab. | cc901ef1 24431a6e
- [Client UI] Movies survive a window switch | Switching to another window during the Kamael movie no longer freezes it; it is now encoded like the client's own movies. | 05eb59f

## 2026-11-14
- [GM tools] Admin tab in Server Management | Shutdown, restart and "shutdown all" (game and login server) with saved countdowns and a double-press safety, plus every GM tool as a button with a tooltip. | cc75a3f1 0fbd610e
- [GM tools] Announcements that work on the Classic client | Log-in announcements now show, can be edited in place, keep their line breaks after a restart, and survive a server deploy. | 43d105e5 802d03bb 43169b2c 5690766a f852332c | shots: 2026-11-14 200038
- [Client UI] Text boxes that start filled in | HTML text boxes can open with text in them, so editing an announcement means changing a letter instead of retyping it. | 7f2eb4c cfae2f3e
- [Login & servers] No more test messages at log-in | The two leftover test lines every player saw when entering the world are gone. | 6106cdf3

## 2026-11-13
- [Events] Change of Heart event | Sprockets the Cat stands in every town, monsters drop heart pieces, and players trade them in a rock, paper, scissors game for prizes; GMs start, stop and place it in game. | a2fe26cc 531cd586 9eec934b 3ce6da17 | shots: 2026-11-13 215535
- [Login & servers] Login errors without crashes | A wrong password or a banned account shows its proper message instead of closing the client. | c39e04e c50504cb
- [Pets & summons] Pets and servitors behave | Pets run, striders can be mounted, Stop and Move to target work, item counts update, and servitor healing shows its numbers. | 5e993890 8d53f074 2d1c3ae9 813dd639 68672f16 7bebb8e0
- [Camera & movement] Steadier keyboard walking | Tapping W at a wall no longer slides the character along it, and holding W in the open no longer stops at random. | b4fae466 acf3305e
- [Login & servers] Server list keeps its place | A Classic server stays in the Classic list while it is loading or down. | 4f6c501f

## 2026-11-12
- [Combat & skills] Critical heals | Classic critical heals are available behind a switch, with their floating label. | 3cd287b7
- [Combat & skills] Servitor damage numbers | Damage numbers now show on servitors, and Immunity is labelled correctly. | b8cdae2e
- [Items & inventory] Live enchant changes | A GM's enchant change appears at once in the owner's inventory. | 3cd5ecc8
- [Quests & tutorial] Full quest list in World Info | The World Info quest list shows every quest the client knows. | e5d35265
