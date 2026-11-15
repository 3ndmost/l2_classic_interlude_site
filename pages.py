"""The Coverage and Classic features tabs (HTML), from extras.py and the scorecard."""
import html
import math
import os
import re

import extras

e = html.escape

PACKET_COLORS = {'Connected': 'done', 'Classic replacement': 'prog', 'Handled another way': 'build', 'Never sent by aCis': 'none',
	'GM viewer': 'part', 'Obsolete': 'line2', 'Not connected': 'wait'}
PACKET_NOTES = {
	'Connected': 'translated to a Classic packet, allowed through, or switching its layout on the protocol',
	'Classic replacement': 'a Classic* class of the same name is sent instead',
	'Handled another way': 'covered by other packets',
	'Never sent by aCis': 'the class exists in aCis but no code sends it',
	'GM viewer': "GM windows (Alt+G) with no Classic version yet",
	'Obsolete': 'version and anti-cheat checks',
	'Not connected': 'aCis sends it and the Classic client never gets it',
}
GAP_NOTES = {
	'BoatSay': "boat captains' announcements (departure, arrival)",
	'ExGetBossRecord': 'the raid point record; the Classic client has no raid point window',
	'ExPlayScene': 'the movie of quest 127 only',
	'ShowPCCafeCouponShowUI': 'the PC Cafe coupon window (PC Cafe points are off by default)',
}
STATE_COLORS = {'tested': 'done', 'mostly': 'prog', 'partly': 'part', 'untested': 'wait', 'unchecked': 'none'}
STATE_LABELS = {'tested': 'Tested', 'mostly': 'Mostly tested', 'partly': 'Partly tested', 'untested': 'Code ready, untested', 'unchecked': 'Not checked'}


def donut(parts, label, sub):
	"""parts: [(name, value, colour token)] -> SVG donut with the total in the middle, and its legend."""
	total = sum(v for _, v, _ in parts) or 1
	r, w, c = 70, 26, 2 * math.pi * 70
	svg = '<svg viewBox="0 0 200 200" class="donut" role="img" aria-label="%s">' % e(label)
	svg += '<circle cx="100" cy="100" r="%d" fill="none" stroke="var(--line)" stroke-width="%d"/>' % (r, w)
	at = 0.0
	for name, v, col in parts:
		if not v:
			continue
		length = c * v / total
		svg += '<circle cx="100" cy="100" r="%d" fill="none" stroke="var(--%s)" stroke-width="%d" stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f" transform="rotate(-90 100 100)"><title>%s: %s</title></circle>' % (
			r, col, w, length, c - length, -at, e(name), v)
		at += length
	svg += '<text x="100" y="98" text-anchor="middle" class="dnum">%s</text><text x="100" y="118" text-anchor="middle" class="dsub">%s</text></svg>' % (e(label), e(sub))
	legend = ''.join('<li><span class="sw" style="background:var(--%s)"></span><span class="lname">%s</span><span class="lval">%s</span></li>' % (col, e(n), v) for n, v, col in parts if v)
	return '<div class="chartbox">%s<ul class="dlegend">%s</ul></div>' % (svg, legend)


def coverage(rows):
	p = extras.packets()
	total = sum(len(v) for v in p.values())
	parts = [(g, len(p[g]), PACKET_COLORS[g]) for g in extras.GROUPS]
	by_state = [(STATE_LABELS[s], sum(1 for r in rows if r[2] == s), STATE_COLORS[s]) for s in STATE_LABELS]
	by_size = [(STATE_LABELS[s], sum(r[1] for r in rows if r[2] == s), STATE_COLORS[s]) for s in STATE_LABELS]
	tested_share = round(100 * sum(r[1] for r in rows if r[2] in ('tested', 'mostly')) / (sum(r[1] for r in rows) or 1))

	out = '<p class="lede">How much of Interlude reaches the Classic client, measured from the server code and from the test record. A packet with a Classic path is not proof that it works: the test states below say what was actually played.</p>'
	out += '<div class="tiles">'
	for v, l in [(total, 'aCis server packets'), (len(p['Connected']) + len(p['Classic replacement']) + len(p['Handled another way']), 'reach the Classic client'),
			(extras.classic_packet_count(), 'Classic packets written'), (len(p['Not connected']), 'still not connected'),
			(len(rows), 'game systems scored'), (extras.quests(), 'quests on the server')]:
		out += '<div class="tile"><div class="num">%s</div><div class="lbl">%s</div></div>' % (v, e(l))
	out += '</div>'

	out += '<div class="charts">'
	out += '<figure><figcaption>Server packets</figcaption>%s</figure>' % donut(parts, str(total), 'packets')
	out += '<figure><figcaption>Game systems by test state</figcaption>%s</figure>' % donut(by_state, str(len(rows)), 'systems')
	out += '<figure><figcaption>Share of the game (by system size)</figcaption>%s</figure>' % donut(by_size, '%d%%' % tested_share, 'tested or mostly')
	out += '</div>'

	out += '<h2 class="gap">Server packets, group by group</h2><div class="groups">'
	for g in extras.GROUPS[1:]:
		names = p[g]
		if not names:
			continue
		items = ''.join('<li><code>%s</code>%s</li>' % (e(n), (' <span class="why">%s</span>' % e(GAP_NOTES.get(n) or extras.OTHER_WAY.get(n, ''))) if (GAP_NOTES.get(n) or extras.OTHER_WAY.get(n)) else '') for n in names)
		out += '<section class="col"><h3><span class="dot" style="background:var(--%s)"></span>%s <span class="cnt">%d</span></h3><p class="why">%s</p><ul class="plain">%s</ul></section>' % (PACKET_COLORS[g], e(g), len(names), e(PACKET_NOTES[g]), items)
	out += '</div><p class="note2">%d packets are connected (%s) and not listed one by one.</p>' % (len(p['Connected']), e(PACKET_NOTES['Connected']))

	out += '<h2 class="gap">Game systems still open</h2><div class="groups">'
	for s in ('unchecked', 'untested', 'partly', 'mostly'):
		sel = [r for r in rows if r[2] == s]
		if not sel:
			continue
		items = ''.join('<li><strong>%s</strong>%s</li>' % (e(r[0]), ' <span class="why">%s</span>' % e(r[3]) if r[3] else '') for r in sel)
		out += '<section class="col"><h3><span class="dot" style="background:var(--%s)"></span>%s <span class="cnt">%d</span></h3><ul class="plain">%s</ul></section>' % (STATE_COLORS[s], STATE_LABELS[s], len(sel), items)
	out += '</div>'

	out += ('<h2 class="gap">What these numbers cannot tell</h2><ul class="caveats">'
		'<li>Tests are recorded per game system, not per packet, so there is no count of tested packets.</li>'
		'<li>The client\'s own requests were not counted: the client\'s request table did not line up with the server\'s routing code, so that figure was left out rather than guessed.</li>'
		'<li>%d quests run on the server; the quest journal, markers and a handful of quests were played through on this client, most quests were not.</li>'
		'<li>Gameplay rules are aCis\'s (the Interlude reference) and are not scored: this page measures whether each system works through the Classic client.</li></ul>') % extras.quests()
	return out


def additions():
	out = '<p class="lede">Everything the project adds to Interlude: Classic client features and project extras. Most have a switch in the server\'s config/classic_features.properties; the value shown is the default the server ships with.</p>'

	switches = extras.classic_switches()
	out += '<h2>Classic features and their switches <span class="cnt">%d switches</span></h2><div class="acc">' % sum(len(s[2]) for s in switches)
	for k, (title, intro, items) in enumerate(switches):
		out += '<details class="acard"%s><summary><span class="atitle">%s</span><span class="cnt">%d</span></summary>' % (' open' if k == 0 else '', e(title), len(items))
		if intro:
			out += '<p class="why">%s</p>' % e(intro)
		out += '<div class="tablewrap"><table class="score"><tbody>'
		for key, value, desc in items:
			out += '<tr><td><code>%s</code></td><td class="val">%s</td><td class="note">%s</td></tr>' % (e(key), e(value) or '&nbsp;', e(desc))
		out += '</tbody></table></div></details>'
	out += '</div>'

	added = extras.added_settings()
	if added:
		out += '<h2 class="gap">Events and other added settings</h2><div class="acc">'
		for f, blocks in added.items():
			for title, intro, items in blocks:
				out += '<details class="acard"><summary><span class="atitle">%s</span><span class="cnt">%s · %d</span></summary>' % (e(title), e(f), len(items))
				if intro:
					out += '<p class="why">%s</p>' % e(intro)
				out += '<div class="tablewrap"><table class="score"><tbody>'
				for key, value, desc in items:
					out += '<tr><td><code>%s</code></td><td class="val">%s</td><td class="note">%s</td></tr>' % (e(key), e(value) or '&nbsp;', e(desc))
				out += '</tbody></table></div></details>'
		out += '</div>'

	cmds = extras.gm_commands()
	out += '<h2 class="gap">GM commands added <span class="cnt">%d</span></h2><div class="tablewrap"><table class="score"><thead><tr><th>Command</th><th>Parameters</th><th>What it does</th></tr></thead><tbody>' % len(cmds)
	for name, params, desc in cmds:
		out += '<tr><td><code>%s</code></td><td class="note">%s</td><td>%s</td></tr>' % (e(name), e(params), e(desc))
	out += '</tbody></table></div>'

	npcs = extras.npcs()
	out += '<h2 class="gap">NPCs added <span class="cnt">%d</span></h2><ul class="plain cards">' % len(npcs)
	for nid, name, title in npcs:
		out += '<li><strong>%s</strong> <span class="why">%s · id %s</span></li>' % (e(name), e(title), nid)
	out += '</ul>'

	its = extras.items()
	types = {}
	for i in its:
		types.setdefault(i[1], []).append(i)
	out += '<h2 class="gap">Items added <span class="cnt">%d</span></h2><p class="why">Classic items made server items (tools/classic_picks.py), the Daily Coin and the Color Title.</p><div class="acc">' % len(its)
	for t, lst in sorted(types.items(), key=lambda kv: -len(kv[1])):
		out += '<details class="acard"><summary><span class="atitle">%s</span><span class="cnt">%d</span></summary><ul class="plain cols">%s</ul></details>' % (
			e({'EtcItem': 'Other items', 'Armor': 'Armor and accessories', 'Weapon': 'Weapons'}.get(t, t)), len(lst), ''.join('<li>%s <span class="why">%s</span></li>' % (e(n), i) for i, _, n, _ in lst))
	out += '</div>'

	sk = extras.skills()
	out += '<h2 class="gap">Skills added <span class="cnt">%d</span></h2><ul class="plain cols">%s</ul>' % (len(sk), ''.join('<li>%s <span class="why">%s</span></li>' % (e(n), i) for i, n in sk))

	out += ('<h2 class="gap">Client-side additions</h2><p class="why">Changes in the client files, with no server switch: they come with the client.</p><ul class="caveats">'
		'<li>The 3D character view in the inventory, and the animated or still "N" mark on new items.</li>'
		'<li>The World Info map tables: zone names, regions, raid bosses, hunting grounds.</li>'
		'<li>Quest head markers, and Interlude wording for the system messages.</li>'
		'<li>Engine and window patches: the fishing window and its 3D view, camera zoom limits from the server, keyboard walking fixes, the lift camera, text boxes that start filled in, and more (listed in the change log under Client).</li></ul>')
	return out
