# Daily highlights

A day written here replaces the automatic picks on the Highlights tab. One "## yyyy-mm-dd" heading per day, then one
line per highlight:

    - [Area] Title | Description | commit commit ...

The area shows its icon (areas as in build.py AREAS: Olympiad, Pets & summons, Events, Login & servers, GM tools,
Camera & movement, Combat & skills, Items & inventory, Quests & tutorial, Clan & siege, "Chat, mail & friends",
Maps & zones, Client UI, Other). The commits (their first characters are enough) become "More in the change log" links.

## 2026-11-14
- [GM tools] Admin tab in Server Management | Shutdown, restart and "shutdown all" (game and login server) with saved countdowns and a double-press safety, plus every GM tool as a button with a tooltip. | cc75a3f1 0fbd610e
- [GM tools] Announcements that work on the Classic client | Log-in announcements now show, can be edited in place, keep their line breaks after a restart, and survive a server deploy. | 43d105e5 802d03bb 43169b2c 5690766a f852332c
- [Client UI] Text boxes that start filled in | HTML text boxes can open with text in them, so editing an announcement means changing a letter instead of retyping it. | 7f2eb4c cfae2f3e
- [Login & servers] No more test messages at log-in | The two leftover test lines every player saw when entering the world are gone. | 6106cdf3

## 2026-11-13
- [Events] Change of Heart event | Sprockets the Cat stands in every town, monsters drop heart pieces, and players trade them in a rock, paper, scissors game for prizes; GMs start, stop and place it in game. | a2fe26cc 531cd586 9eec934b 3ce6da17
- [Login & servers] Login errors without crashes | A wrong password or a banned account shows its proper message instead of closing the client. | c39e04e c50504cb
- [Pets & summons] Pets and servitors behave | Pets run, striders can be mounted, Stop and Move to target work, item counts update, and servitor healing shows its numbers. | 5e993890 8d53f074 2d1c3ae9 813dd639 68672f16 7bebb8e0
- [Camera & movement] Steadier keyboard walking | Tapping W at a wall no longer slides the character along it, and holding W in the open no longer stops at random. | b4fae466 acf3305e
- [Login & servers] Server list keeps its place | A Classic server stays in the Classic list while it is loading or down. | 4f6c501f

## 2026-11-12
- [Combat & skills] Critical heals | Classic critical heals are available behind a switch, with their floating label. | 3cd287b7
- [Combat & skills] Servitor damage numbers | Damage numbers now show on servitors, and Immunity is labelled correctly. | b8cdae2e
- [Items & inventory] Live enchant changes | A GM's enchant change appears at once in the owner's inventory. | 3cd5ecc8
- [Quests & tutorial] Full quest list in World Info | The World Info quest list shows every quest the client knows. | e5d35265
