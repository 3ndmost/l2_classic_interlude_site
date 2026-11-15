"""Build the project site: one page with the commit log, statistics and the feature status.

  python build.py                 writes docs/index.html (GitHub Pages: branch main, folder /docs)
  python build.py --fragment F    also writes the page body only (for a claude.ai artifact preview)

Reads the dev branch of the three repos next to this folder (server, client, server_build) and the feature table of
l2_classic_interlude_server_build/docs/FEATURE_CHECKLIST.md (the "| Fnn |" rows only: id, feature, state).
Private details never reach the page: e-mail addresses, IPv4 addresses and Windows user folders are removed from every
text, the Co-Authored-By lines are dropped, and commit authors are not shown.
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPOS = [
	('server', 'l2_classic_interlude_server', 'Server'),
	('client', 'l2_classic_interlude_client', 'Client'),
	('build', 'l2_classic_interlude_server_build', 'Runtime'),
]
LEDGER = os.path.join(ROOT, 'l2_classic_interlude_server_build', 'docs', 'FEATURE_CHECKLIST.md')

EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
IPV4 = re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b')
USERDIR = re.compile(r'([A-Za-z]:[\\/]+Users[\\/]+)[^\\/\s]+', re.I)

# Areas, first match wins; matched against the subject, the body and the file paths.
AREAS = [
	('Olympiad', r'olympiad|hero|stadium|spectat'),
	('Pets & summons', r'\bpets?\b|summon|servitor|strider|wolf'),
	('Events', r'change of heart|sprockets|events\.properties|seasonal event'),
	('Login & servers', r'login|server list|password|ban(ned)? account|loginserver'),
	('GM tools', r'\bgm\b|admin|(?<![:/])//\w|announce|server management|board test|talkscan|ratetest'),
	('Camera & movement', r'camera|zoom|wasd|keyboard|movement|move |swim|water|falling|boat|lift'),
	('Combat & skills', r'skill|damage|heal|attack|critical|buff|effect|enchant|cast'),
	('Items & inventory', r'item|inventory|weapon|armor|multisell|shop|warehouse|craft|recipe|augment|henna'),
	('Quests & tutorial', r'quest|tutorial|daily mission|mark'),
	('Clan & siege', r'clan|alliance|siege|castle|manor|clan hall'),
	('Chat, mail & friends', r'chat|mail|friend|whisper|party|message'),
	('Maps & zones', r'\bmap|zone|region|territor|geodata|dungeon'),
	('Client UI', r'window|interface\.u|xdat|ugx|tooltip|ui\b|button|dialog|html'),
]
AREAS = [(name, re.compile(rx, re.I)) for name, rx in AREAS]

# One game icon per area (icons/, 32 x 32 item icons of the client), embedded in the page.
ICONS = {
	'Olympiad': 'weapon_he_two_handed_sword_of_hero_i00', 'Pets & summons': 'etc_summon_wolf_r_01', 'Events': 'etc_heart_i00',
	'Login & servers': 'etc_key_i00', 'GM tools': 'etc_bugle_i00', 'Camera & movement': 'armor_boots_i00',
	'Combat & skills': 'time_weapon_crimson_sword_i00', 'Items & inventory': 'etc_handbag_i00', 'Quests & tutorial': 'bookmark_scroll_i00',
	'Clan & siege': 'weapon_fort_flag_i00', 'Chat, mail & friends': 'etc_letter_envelope_i00', 'Maps & zones': 'etc_map_ivory_i00',
	'Client UI': 'etc_spellbook_gray_i00', 'Other': 'etc_broken_crystal_silver_i00',
}


def icon_uris():
	import base64
	out = {}
	for area, name in ICONS.items():
		path = os.path.join(HERE, 'icons', name + '.png')
		if os.path.exists(path):
			out[area] = 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode('ascii')
	return out


def slug(area):
	return re.sub(r'[^a-z]+', '-', area.lower()).strip('-')


def icon_css(uris):
	"""Each icon once, as a class: .i-<area> (the page shows an area's icon many times)."""
	return ''.join('.i-%s { background-image: url(%s) }\n' % (slug(a), u) for a, u in uris.items())


def ico(uris, area, size=20):
	return '<span class="ico i-%s" style="width:%dpx;height:%dpx" aria-hidden="true"></span>' % (slug(area), size, size) if area in uris else ''


def clean(text):
	text = '\n'.join(line for line in text.splitlines() if not line.lower().startswith('co-authored-by'))
	text = EMAIL.sub('[e-mail removed]', text)
	text = IPV4.sub('[IP removed]', text)
	text = USERDIR.sub(r'\1…', text)
	return text.strip()


def git(repo, *args):
	return subprocess.run(['git', '-C', os.path.join(ROOT, repo)] + list(args), capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def commits():
	out = []
	for key, folder, _ in REPOS:
		raw = git(folder, 'log', 'dev', '--numstat', '--date=iso-strict', '--format=%x1e%H%x1f%ad%x1f%s%x1f%b%x1f')
		for record in raw.split('\x1e')[1:]:
			sha, date, subject, body, stats = record.split('\x1f', 4)
			added = removed = files = 0
			paths = []
			for line in stats.strip().splitlines():
				parts = line.split('\t')
				if len(parts) != 3:
					continue
				files += 1
				paths.append(parts[2])
				added += int(parts[0]) if parts[0].isdigit() else 0
				removed += int(parts[1]) if parts[1].isdigit() else 0
			subject, body = clean(subject), clean(body)
			hay = subject + '\n' + body[:600] + '\n' + ' '.join(paths)
			area = next((name for name, rx in AREAS if rx.search(subject)), None) or next((name for name, rx in AREAS if rx.search(hay)), 'Other')
			out.append({'r': key, 'h': sha[:8], 'd': date[:19], 's': subject, 'b': body, 'a': area, 'f': files, 'p': added, 'm': removed})
	out.sort(key=lambda c: c['d'], reverse=True)
	return out


def features():
	"""The feature table: (id, feature, implemented, confirmed, group)."""
	rows = []
	if not os.path.exists(LEDGER):
		return rows
	for line in open(LEDGER, encoding='utf-8'):
		m = re.match(r'\|\s*(F\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|', line)
		if not m:
			continue
		fid, name, required, implemented, confirmed = (clean(x.strip().replace('**', '')) for x in m.groups())
		c, i, r = confirmed.lower(), implemented.lower(), required.lower()
		if r.startswith('no'):
			group = 'Out of scope'
		elif c.startswith(('yes', 'tested ok')):
			group = 'Done'
		elif 'awaiting' in c:
			group = 'Waiting for test'
		elif c.startswith(('partial', 'partly')):
			group = 'Partly done'
		elif 'not audited' in i or c.startswith('no'):
			group = 'Not started'
		else:
			group = 'In progress'
		rows.append({'id': fid, 'n': name, 'i': implemented, 'c': confirmed, 'g': group})
	return rows


def week_chart(data):
	"""Commits per ISO week, stacked by repo, as SVG (colours from the page's tokens)."""
	weeks = {}
	for c in data:
		d = datetime.date.fromisoformat(c['d'][:10])
		monday = d - datetime.timedelta(days=d.weekday())
		weeks.setdefault(monday, {'server': 0, 'client': 0, 'build': 0})[c['r']] += 1
	if not weeks:
		return ''
	first, last = min(weeks), max(weeks)
	cols = []
	d = first
	while d <= last:
		cols.append((d, weeks.get(d, {'server': 0, 'client': 0, 'build': 0})))
		d += datetime.timedelta(days=7)
	top = max(sum(v.values()) for _, v in cols)
	step = 10 if top <= 60 else 20 if top <= 120 else 50
	ymax = ((top + step - 1) // step) * step
	w, h, left, bottom, topm = 760, 240, 40, 28, 12
	bw = (w - left - 8) / len(cols)
	sy = (h - bottom - topm) / ymax
	parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Commits per week, by repository">' % (w, h)]
	for t in range(0, ymax + 1, step):
		y = h - bottom - t * sy
		parts.append('<line class="grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="axis" x="%d" y="%.1f" text-anchor="end">%d</text>' % (left, w - 4, y, y, left - 6, y + 4, t))
	for k, (monday, v) in enumerate(cols):
		x = left + k * bw + 1
		y = h - bottom
		for repo in ('server', 'client', 'build'):
			n = v[repo]
			if n:
				parts.append('<rect class="bar-%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"><title>Week of %s: %d %s</title></rect>' % (repo, x, y - n * sy, max(bw - 2, 1), n * sy, monday.isoformat(), n, repo))
				y -= n * sy
		if monday.day <= 7:
			parts.append('<text class="axis" x="%.1f" y="%d">%s</text>' % (x, h - 8, monday.strftime('%b')))
	parts.append('</svg>')
	return ''.join(parts)


# Overall progress: what each feature state counts for (out of scope does not count).
WEIGHTS = {'Done': 1.0, 'Waiting for test': 0.8, 'Partly done': 0.6, 'In progress': 0.4, 'Not started': 0.0}

HIGHLIGHTS_FILE = os.path.join(HERE, 'highlights.md')
PER_DAY = 5
# Commits that are housekeeping, not progress: never a highlight.
MINOR = re.compile(r'^(document|docs?\b|record|note|update (the )?(docs|readme|ledger|manual)|merge|revert|restore|correct the .*(comment|note)|add(ed)? \.git|update \.git|remove (the )?(temporary )?debug|leave .* room|tidy|rename)', re.I)


def progress(feats):
	counted = [f for f in feats if f['g'] in WEIGHTS]
	return round(100 * sum(WEIGHTS[f['g']] for f in counted) / len(counted)) if counted else 0


def manual_highlights():
	"""highlights.md: '## yyyy-mm-dd' then '- text' lines; a day written there replaces the automatic picks."""
	out, day = {}, None
	if os.path.exists(HIGHLIGHTS_FILE):
		for line in open(HIGHLIGHTS_FILE, encoding='utf-8'):
			m = re.match(r'##\s*(\d{4}-\d{2}-\d{2})', line)
			if m:
				day = m.group(1)
				out[day] = []
			elif day and line.strip().startswith('- '):
				out[day].append(clean(line.strip()[2:]))
	return out


def score(c):
	if MINOR.search(c['s']) or c['r'] == 'build':
		return -1
	size = c['p'] + c['m'] + 40 * c['f']
	s = len(str(size)) + (2 if c['a'] != 'Other' else 0) + (1 if len(c['b']) > 400 else 0)
	if re.match(r'(add|show|let|make|give|start|keep|stop|fix)\b', c['s'], re.I):
		s += 2
	return s


def highlights(data):
	"""Per day, newest first: (day, [(area, text)], number of other changes, hand-written or not)."""
	manual = manual_highlights()
	days = {}
	for c in data:
		days.setdefault(c['d'][:10], []).append(c)
	out = []
	for day in sorted(days, reverse=True):
		commits = days[day]
		if day in manual:
			# "- [Area] text" gives a hand-written line its area (and icon).
			items = []
			for t in manual[day]:
				m = re.match(r'\[([^\]]+)\]\s*(.*)', t)
				items.append((m.group(1), m.group(2)) if m else ('', t))
			out.append((day, items, len(commits), True))
			continue
		ranked = sorted((c for c in commits if score(c) >= 0), key=score, reverse=True)[:PER_DAY]
		if ranked:
			out.append((day, [(c['a'], c['s']) for c in ranked], len(commits), False))
	return out


def page(data, feats):
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
	by_repo = {k: sum(1 for c in data if c['r'] == k) for k, _, _ in REPOS}
	areas = {}
	for c in data:
		areas[c['a']] = areas.get(c['a'], 0) + 1
	area_rows = sorted(areas.items(), key=lambda kv: -kv[1])
	amax = max(areas.values()) if areas else 1
	groups = ['Done', 'Partly done', 'Waiting for test', 'In progress', 'Not started', 'Out of scope']
	counts = {g: sum(1 for f in feats if f['g'] == g) for g in groups}
	first = min(c['d'] for c in data)[:10] if data else ''
	days = (datetime.date.today() - datetime.date.fromisoformat(first)).days + 1 if first else 0
	lines = sum(c['p'] + c['m'] for c in data)

	e = html.escape
	tiles = ''.join('<div class="tile"><div class="num">%s</div><div class="lbl">%s</div></div>' % (e(str(v)), e(l)) for v, l in [
		(len(data), 'commits'), (by_repo['server'], 'server commits'), (by_repo['client'], 'client commits'),
		(counts['Done'], 'features done'), (days, 'days since the first commit'), ('{:,}'.format(lines), 'lines changed')])
	uris = icon_uris()
	area_html = ''.join('<div class="arow"><span class="aname">%s%s</span><span class="abar"><span style="width:%.1f%%"></span></span><span class="acount">%d</span></div>' % (ico(uris, n), e(n), 100.0 * v / amax, v) for n, v in area_rows)
	board = ''
	for g in groups:
		items = [f for f in feats if f['g'] == g]
		if not items:
			continue
		board += '<section class="col"><h3><span class="dot g-%s"></span>%s <span class="cnt">%d</span></h3><ul>' % (re.sub(r'\W+', '-', g.lower()), e(g), len(items))
		for f in items:
			board += '<li><span class="fid">%s</span><span class="fname">%s</span><span class="fstate">%s</span></li>' % (e(f['id']), e(f['n']), e(f['c'][:140]))
		board += '</ul></section>'

	pct = progress(feats)
	prog = ('<div class="progress"><div class="ptop"><span class="pnum">~%d%%</span><span class="plbl">overall progress (approximate)</span></div>'
		'<div class="pbar" role="progressbar" aria-valuenow="%d" aria-valuemin="0" aria-valuemax="100"><span style="width:%d%%"></span></div>'
		'<p class="pnote">Counted from the %d features in scope: done 100%%, waiting for test 80%%, partly done 60%%, in progress 40%%, not started 0%%. '
		'The features differ a lot in size, so this is a rough guide, not a measurement.</p></div>') % (pct, pct, pct, sum(1 for f in feats if f['g'] in WEIGHTS))

	hl = ''
	for day, items, total, manual in highlights(data):
		label = datetime.date.fromisoformat(day).strftime('%A %d %B %Y')
		hl += '<article class="hday"><h3>%s <span class="cnt">%d change%s%s</span></h3><ul>' % (e(label), total, '' if total == 1 else 's', '' if manual else ' · picked automatically')
		for area, text in items:
			hl += '<li>%s<span>%s%s</span></li>' % (ico(uris, area, 24) if area else '', '<span class="harea">%s</span>' % e(area) if area else '', e(text))
		hl += '</ul></article>'

	data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
	return TEMPLATE.replace('%NOW%', now).replace('%TILES%', tiles).replace('%CHART%', week_chart(data)).replace('%AREAS%', area_html) \
		.replace('%BOARD%', board).replace('%DATA%', data_json).replace('%FIRST%', first).replace('%PROGRESS%', prog).replace('%HIGHLIGHTS%', hl) \
		.replace('%ICONS%', json.dumps({a: slug(a) for a in uris})).replace('%ICONCSS%', icon_css(uris))


TEMPLATE = r'''<title>Classic Interlude Devlog</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap">
<style>
/* Layout: one column, summary first (tiles, weekly chart, areas), then the feature board, then the searchable log. */
:root {
  --bg: #f3f4f1; --surface: #ffffff; --fg: #1d2421; --muted: #5d6763; --line: #d9ddd7;
  --gold: #a87a12; --server: #2b7a78; --client: #b8862b; --build: #6b6fa8;
  --done: #2e7d4f; --part: #b8862b; --wait: #c2581f; --prog: #3d6fb4; --none: #8a918d;
  --display: "Space Grotesk", "Segoe UI", system-ui, sans-serif;
  --body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #141917; --surface: #1c2320; --fg: #e4e8e5; --muted: #9aa49f; --line: #2d3632;
  --gold: #d9ad4a; --server: #4fb3ae; --client: #d9a84a; --build: #9599d6;
  --done: #5cc189; --part: #d9a84a; --wait: #ec8a52; --prog: #77a6e6; --none: #7c8580; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #141917; --surface: #1c2320; --fg: #e4e8e5; --muted: #9aa49f; --line: #2d3632;
  --gold: #d9ad4a; --server: #4fb3ae; --client: #d9a84a; --build: #9599d6;
  --done: #5cc189; --part: #d9a84a; --wait: #ec8a52; --prog: #77a6e6; --none: #7c8580; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); margin: 0 }
.wrap { max-width: 1080px; margin: 0 auto; padding-block: 32px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 40px }
h1, h2, h3 { font-family: var(--display); text-wrap: balance; margin: 0 }
h1 { font-size: clamp(28px, 5vw, 44px); line-height: 1.1 }
h2 { font-size: 22px; margin-bottom: 14px }
h3 { font-size: 15px }
.eyebrow { font: 500 12px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--gold) }
.lede { max-width: 68ch; color: var(--muted); margin: 10px 0 0 }
.meta { font: 12px var(--mono); color: var(--muted); margin-top: 10px }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px }
.tile { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 14px 16px }
.num { font: 700 28px var(--display); font-variant-numeric: tabular-nums }
.lbl { font-size: 13px; color: var(--muted) }
.two { display: grid; grid-template-columns: 3fr 2fr; gap: 24px }
.two > * { min-width: 0 }
@media (max-width: 800px) { .two { grid-template-columns: 1fr } }
.chart svg { width: 100%; height: auto; display: block }
.grid { stroke: var(--line); stroke-width: 1 }
.axis { fill: var(--muted); font: 10px var(--mono) }
.bar-server { fill: var(--server) } .bar-client { fill: var(--client) } .bar-build { fill: var(--build) }
.legend { display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; color: var(--muted); margin-top: 8px }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: -1px }
.sw.server { background: var(--server) } .sw.client { background: var(--client) } .sw.build { background: var(--build) }
.arow { display: grid; grid-template-columns: 150px 1fr 40px; gap: 10px; align-items: center; font-size: 13px; padding: 3px 0 }
.abar { height: 8px; background: var(--line); border-radius: 4px; overflow: hidden }
.abar span { display: block; height: 100%; background: var(--gold) }
.acount { text-align: right; font: 12px var(--mono); font-variant-numeric: tabular-nums; color: var(--muted) }
.board { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px }
.col { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 14px 16px; min-width: 0 }
.col h3 { display: flex; align-items: center; gap: 8px; margin-bottom: 8px }
.cnt { font: 12px var(--mono); color: var(--muted) }
.dot { width: 9px; height: 9px; border-radius: 50% }
.g-done { background: var(--done) } .g-partly-done { background: var(--part) } .g-waiting-for-test { background: var(--wait) }
.g-in-progress { background: var(--prog) } .g-not-started, .g-out-of-scope { background: var(--none) }
.col ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px }
.col li { display: grid; grid-template-columns: 40px 1fr; column-gap: 8px; font-size: 13px }
.fid { font: 12px var(--mono); color: var(--muted); grid-row: span 2 }
.fstate { color: var(--muted); font-size: 12px }
.controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 14px }
.controls input, .controls select { font: 14px var(--body); padding: 7px 10px; border: 1px solid var(--line); border-radius: 6px; background: var(--surface); color: var(--fg) }
.controls input { flex: 1 1 240px; min-width: 0 }
.chip { font: 13px var(--body); padding: 6px 12px; border-radius: 999px; border: 1px solid var(--line); background: var(--surface); color: var(--fg); cursor: pointer }
.chip[aria-pressed="true"] { border-color: var(--fg); font-weight: 600 }
.chip:focus-visible, .controls input:focus-visible, .controls select:focus-visible, summary:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px }
.count { font: 12px var(--mono); color: var(--muted) }
.day { font: 600 13px var(--display); color: var(--muted); margin: 18px 0 6px; padding-bottom: 4px; border-bottom: 1px solid var(--line) }
details { border-bottom: 1px solid var(--line) }
summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: 66px 74px 1fr auto; gap: 10px; align-items: baseline; padding: 8px 0 }
summary::-webkit-details-marker { display: none }
.repo { font: 500 11px var(--mono); text-transform: uppercase; letter-spacing: .06em }
.repo.server { color: var(--server) } .repo.client { color: var(--client) } .repo.build { color: var(--build) }
.sha { font: 12px var(--mono); color: var(--muted) }
.subj { min-width: 0 }
.area { font-size: 12px; color: var(--muted); white-space: nowrap }
.body { white-space: pre-wrap; font: 13px/1.6 var(--mono); color: var(--muted); padding: 0 0 14px 150px; overflow-x: auto }
.stat { font: 12px var(--mono); color: var(--muted); padding: 0 0 8px 150px }
@media (max-width: 640px) {
  summary { grid-template-columns: 56px 1fr; }
  .sha, .area { display: none }
  .body, .stat { padding-left: 0 }
  .arow { grid-template-columns: 110px 1fr 34px }
}
#more { margin-top: 16px }
.progress { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 18px 20px; display: grid; gap: 10px }
.ptop { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap }
.pnum { font: 700 40px var(--display); font-variant-numeric: tabular-nums; color: var(--gold) }
.plbl { font: 600 15px var(--display) }
.pbar { height: 12px; background: var(--line); border-radius: 6px; overflow: hidden }
.pbar span { display: block; height: 100%; background: var(--done) }
.pnote { margin: 0; font-size: 13px; color: var(--muted); max-width: 80ch }
.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); flex-wrap: wrap; margin-bottom: -24px }
.tab { font: 600 15px var(--display); background: none; border: 0; border-bottom: 3px solid transparent; color: var(--muted); padding: 10px 16px; cursor: pointer }
.tab[aria-selected="true"] { color: var(--fg); border-bottom-color: var(--gold) }
.tab:focus-visible { outline: 2px solid var(--gold); outline-offset: -2px }
.hlist { display: grid; gap: 14px; max-width: 860px }
.hday { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 14px 18px }
.hday h3 { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 8px }
.hday ul { margin: 0; padding-left: 18px; display: grid; gap: 5px }
.ico { display: inline-block; vertical-align: middle; margin-right: 8px; border-radius: 3px; flex: none; background-size: cover }
%ICONCSS%
.aname { display: flex; align-items: center; min-width: 0 }
.area .ico { margin-right: 6px }
.hday li { display: flex; align-items: flex-start; gap: 2px; list-style: none }
.hday li .ico { margin-top: -1px }
.hday ul { padding-left: 0 }
.harea { font: 500 11px var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--gold); margin-right: 8px }
</style>

<div class="wrap">
  <header>
    <div class="eyebrow">Lineage II · Classic 2.5 client · Interlude server</div>
    <h1>Classic Interlude Devlog</h1>
    <p class="lede">The Classic Zaken client (protocol 110) running on an aCis Interlude server: the client gets the packets and windows it expects, while the gameplay stays Interlude. This page lists every change to the server, the client and the runtime, with the state of each feature.</p>
    <div class="meta">Updated %NOW% · history since %FIRST%</div>
  </header>

  %PROGRESS%

  <section class="tiles" aria-label="Totals">%TILES%</section>

  <section class="two">
    <div class="chart">
      <h2>Commits per week</h2>
      %CHART%
      <div class="legend"><span><span class="sw server"></span>Server</span><span><span class="sw client"></span>Client</span><span><span class="sw build"></span>Runtime</span></div>
    </div>
    <div>
      <h2>Work by area</h2>
      %AREAS%
    </div>
  </section>

  <nav class="tabs" role="tablist" aria-label="Views">
    <button class="tab" role="tab" id="tab-highlights" data-view="highlights" aria-controls="highlights">Highlights</button>
    <button class="tab" role="tab" id="tab-status" data-view="status" aria-controls="status">Feature status</button>
    <button class="tab" role="tab" id="tab-log" data-view="log" aria-controls="log-view">Change log</button>
  </nav>

  <section class="view" id="highlights" role="tabpanel" aria-labelledby="tab-highlights">
    <p class="lede">The main progress of each day, in a few lines. The full list is in the Change log.</p>
    <div class="hlist">%HIGHLIGHTS%</div>
  </section>

  <section class="view" id="status" role="tabpanel" aria-labelledby="tab-status" hidden>
    <div class="board">%BOARD%</div>
  </section>

  <section class="view" id="log-view" role="tabpanel" aria-labelledby="tab-log" hidden>
    <div class="controls">
      <input id="q" type="search" placeholder="Search commits (title or explanation)" aria-label="Search commits">
      <select id="area" aria-label="Area"><option value="">All areas</option></select>
      <button class="chip" data-repo="server" aria-pressed="true">Server</button>
      <button class="chip" data-repo="client" aria-pressed="true">Client</button>
      <button class="chip" data-repo="build" aria-pressed="true">Runtime</button>
      <span class="count" id="count"></span>
    </div>
    <div id="log"></div>
    <button class="chip" id="more" hidden>Show more</button>
  </section>
</div>

<script>
const DATA = %DATA%;
const ICONS = %ICONS%;
const icon = (a) => ICONS[a] ? '<span class="ico i-' + ICONS[a] + '" style="width:18px;height:18px" aria-hidden="true"></span>' : '';
const PAGE = 150;
const repos = { server: true, client: true, build: true };
const names = { server: 'Server', client: 'Client', build: 'Runtime' };
let shown = PAGE, list = DATA;
const $ = (s) => document.querySelector(s);
const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const areaSel = $('#area');
[...new Set(DATA.map((c) => c.a))].sort().forEach((a) => areaSel.add(new Option(a, a)));

function filter() {
  const q = $('#q').value.trim().toLowerCase(), area = areaSel.value;
  list = DATA.filter((c) => repos[c.r] && (!area || c.a === area) && (!q || c.s.toLowerCase().includes(q) || c.b.toLowerCase().includes(q) || c.h.startsWith(q)));
  shown = PAGE;
  render();
}

function render() {
  let out = '', day = '';
  for (const c of list.slice(0, shown)) {
    const d = c.d.slice(0, 10);
    if (d !== day) { day = d; out += '<div class="day">' + new Date(d + 'T12:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + '</div>'; }
    out += '<details><summary><span class="repo ' + c.r + '">' + names[c.r] + '</span><span class="sha">' + c.h + '</span><span class="subj">' + esc(c.s) + '</span><span class="area">' + icon(c.a) + esc(c.a) + '</span></summary>'
      + '<div class="stat">' + c.d.slice(11, 16) + ' · ' + c.f + ' files · +' + c.p + ' −' + c.m + '</div>'
      + (c.b ? '<div class="body">' + esc(c.b) + '</div>' : '') + '</details>';
  }
  $('#log').innerHTML = out || '<p class="count">No commit matches.</p>';
  $('#count').textContent = list.length + ' of ' + DATA.length + ' commits';
  $('#more').hidden = shown >= list.length;
}

$('#q').addEventListener('input', filter);
areaSel.addEventListener('change', filter);
document.querySelectorAll('[data-repo]').forEach((b) => b.addEventListener('click', () => {
  repos[b.dataset.repo] = !repos[b.dataset.repo];
  b.setAttribute('aria-pressed', repos[b.dataset.repo]);
  filter();
}));
$('#more').addEventListener('click', () => { shown += PAGE; render(); });
render();

// Tabs: one view at a time, kept in the address (#highlights, #status, #log).
const VIEWS = { highlights: 'highlights', status: 'status', log: 'log-view' };
function showView() {
  const v = VIEWS[location.hash.slice(1)] ? location.hash.slice(1) : 'highlights';
  for (const [name, id] of Object.entries(VIEWS)) {
    document.getElementById(id).hidden = name !== v;
    document.getElementById('tab-' + name).setAttribute('aria-selected', name === v);
  }
}
document.querySelectorAll('.tab').forEach((t) => t.addEventListener('click', () => { location.hash = t.dataset.view; }));
window.addEventListener('hashchange', showView);
showView();
</script>
'''

FULL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
%s
</body>
</html>
'''


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--fragment')
	a = ap.parse_args()
	data, feats = commits(), features()
	body = page(data, feats)
	os.makedirs(os.path.join(HERE, 'docs'), exist_ok=True)
	open(os.path.join(HERE, 'docs', 'index.html'), 'w', encoding='utf-8').write(FULL % body)
	if a.fragment:
		open(a.fragment, 'w', encoding='utf-8').write(body)
	left = [c['h'] for c in data if EMAIL.search(c['s'] + c['b']) or IPV4.search(c['s'] + c['b'])]
	print('%d commits, %d features, %d KB; private details left: %s' % (len(data), len(feats), len(body) // 1024, left or 'none'))


if __name__ == '__main__':
	main()
