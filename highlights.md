# Daily highlights

A day written here replaces the automatic picks on the Highlights tab. One "## yyyy-mm-dd" heading per day, then one
line per highlight:

    - [Area] Title | Description | commit commit ... | shots: 2026-11-13 215535, 2026-11-14 200038

The area shows its icon (areas as in build.py AREAS: Olympiad, Pets & summons, Events, Login & servers, GM tools,
Camera & movement, Combat & skills, Items & inventory, Quests & tutorial, Clan & siege, "Chat, mail & friends",
Maps & zones, Client UI, Other). The commits (their first characters are enough) become "More in the change log" links. The shots are
Windows screenshots (Pictures/Screenshots, "Screenshot <date> <time>.png"), copied small into docs/shots: check each
one for private details before it goes on the public page.

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
