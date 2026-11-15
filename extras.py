"""Data for the Coverage and Classic features tabs, read from the server repo (see build.py)."""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(os.path.dirname(HERE), 'l2_classic_interlude_server')
JAVA = os.path.join(SERVER, 'aCis_gameserver', 'java', 'net', 'sf', 'l2j', 'gameserver')
CONFIG = os.path.join(SERVER, 'aCis_gameserver', 'config')
DATA = os.path.join(SERVER, 'aCis_datapack', 'data')
FIRST_COMMIT = 'f19a3b8c'   # the aCis source as the project started from it

# Packets with no Classic class that need none, and why (checked 2026-11-15, docs/CLASSIC_GAPS.md).
OBSOLETE = {'GameGuardQuery', 'ExRequestHackShield', 'RequestTimeCheck', 'ExRestartClient'}
OTHER_WAY = {
	'DoorInfo': 'doors go out as StaticObjectInfo', 'DoorStatusUpdate': 'doors go out as StaticObjectInfo',
	'ExPledgeCrestLarge': 'the large crest has its own Classic packets', 'ExFishingHpRegen': 'fishing runs by the FishingMode setting',
	'ExFishingStartCombat': 'fishing runs by the FishingMode setting', 'ExEnchantSkillList': 'skill enchanting uses the Classic enchant window',
}
GROUPS = ['Connected', 'Classic replacement', 'Handled another way', 'Never sent by aCis', 'GM viewer', 'Obsolete', 'Not connected']


EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
IPV4 = re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b')


def _read(path):
	"""A file's text, with e-mail and IPv4 addresses removed (everything here may end up on the public page)."""
	text = open(path, encoding='utf-8', errors='replace').read()
	return IPV4.sub('[IP removed]', EMAIL.sub('[e-mail removed]', text))


def packets():
	"""{group: [names]} for every aCis server packet (Classic* classes excluded)."""
	folder = os.path.join(JAVA, 'network', 'serverpackets')
	client = _read(os.path.join(JAVA, 'network', 'GameClient.java'))
	classic = {f[7:-5].lower() for f in os.listdir(folder) if f.startswith('Classic')}
	sources = {}
	for root, _, files in os.walk(JAVA):
		for f in files:
			if f.endswith('.java'):
				sources[os.path.join(root, f)] = _read(os.path.join(root, f))
	out = {g: [] for g in GROUPS}
	for f in sorted(os.listdir(folder)):
		if not f.endswith('.java') or f.startswith(('Classic', 'Abstract', 'L2GameServerPacket')):
			continue
		name = f[:-5]
		src = sources[os.path.join(folder, f)]
		word = re.compile(r'\b' + name + r'\b')
		if word.search(client) or 'CLASSIC_INTERLUDE' in src or 'ClientProtocol' in src:
			group = 'Connected'
		elif name.lower() in classic or (name.startswith('Ex') and name[2:].lower() in classic):
			group = 'Classic replacement'
		elif name in OTHER_WAY:
			group = 'Handled another way'
		elif not any(word.search(s) for p, s in sources.items() if not p.endswith(os.sep + f)):
			group = 'Never sent by aCis'
		elif name.startswith(('GMView', 'GMHenna', 'Snoop')):
			group = 'GM viewer'
		elif name in OBSOLETE:
			group = 'Obsolete'
		else:
			group = 'Not connected'
		out[group].append(name)
	return out


def classic_packet_count():
	return sum(1 for f in os.listdir(os.path.join(JAVA, 'network', 'serverpackets')) if f.startswith('Classic') and f.endswith('.java'))


def _config_blocks(text):
	"""[(section, intro, [(key, value, description)])] of a .properties file written as '#====' framed section titles
	and '#' comments: a setting's description is the comment paragraph right above it, a section's intro the paragraphs
	before its first setting's own."""
	out, paras, current, in_head = [], [], [], False

	def flush():
		if current:
			paras.append(' '.join(current))
			current.clear()

	for raw in text.splitlines():
		line = raw.strip()
		if line.startswith('#='):
			in_head = not in_head
			continue
		if in_head:
			title = line.lstrip('#').strip()
			if title:
				out.append([title, '', []])
				paras.clear()
				current.clear()
			continue
		if line.startswith('#'):
			body = line[1:].strip()
			if body:
				current.append(body)
			else:
				flush()
			continue
		if not line:
			flush()
			continue
		m = re.match(r'([A-Za-z0-9_.]+)\s*=\s*(.*)', line)
		if m:
			flush()
			if not out:
				out.append(['General', '', []])
			section = out[-1]
			if not section[2] and len(paras) > 1:
				section[1] = ' '.join(paras[:-1])
			section[2].append((m.group(1), m.group(2).strip(), paras[-1] if paras else ''))
			paras.clear()
	return [(t, i, s) for t, i, s in out if s]


def classic_switches():
	path = os.path.join(CONFIG, 'classic_features.properties')
	return _config_blocks(_read(path)) if os.path.exists(path) else []


def added_settings():
	"""{file: [(section, [(key, value, description)])]}: settings of the other config files added since the first commit."""
	out = {}
	for f in sorted(os.listdir(CONFIG)):
		if not f.endswith('.properties') or f in ('classic_features.properties', 'loginserver.properties', 'server.properties'):
			continue
		old = subprocess.run(['git', '-C', SERVER, 'show', FIRST_COMMIT + ':aCis_gameserver/config/' + f], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
		old_keys = set(re.findall(r'^\s*([A-Za-z0-9_.]+)\s*=', old, re.M))
		blocks = []
		for section, intro, items in _config_blocks(_read(os.path.join(CONFIG, f))):
			new = [i for i in items if i[0] not in old_keys]
			if new:
				blocks.append((section, intro, new))
		if blocks:
			out[f] = blocks
	return out


def gm_commands():
	"""[(command, params, description)] added to adminCommands.xml since the first commit."""
	path = 'aCis_datapack/data/xml/adminCommands.xml'
	old = subprocess.run(['git', '-C', SERVER, 'show', FIRST_COMMIT + ':' + path], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
	old_names = set(re.findall(r'name="(admin_[^"]+)"', old))
	out = []
	for m in re.finditer(r'<aCar name="(admin_[^"]+)" accessLevel="\d+" params="([^"]*)" desc="([^"]*)"', _read(os.path.join(SERVER, path))):
		if m.group(1) not in old_names:
			out.append(('//' + m.group(1)[6:], m.group(2), m.group(3).replace('&amp;', '&')))
	return out


def npcs():
	path = os.path.join(DATA, 'xml', 'npcs', '50000-50999.xml')
	return re.findall(r'<npc id="(\d+)"[^>]*?name="([^"]*)" title="([^"]*)"', _read(path)) if os.path.exists(path) else []


def items():
	"""[(id, type, name, file)] of the item files the project added."""
	out = []
	for f in ('13000-13099.xml', '70000-70099.xml', 'classicPicks.xml'):
		path = os.path.join(DATA, 'xml', 'items', f)
		if os.path.exists(path):
			out += [(i, t, n, f) for i, t, n in re.findall(r'<item id="(\d+)" type="(\w+)" name="([^"]*)"', _read(path))]
	return out


def skills():
	out = []
	for f in ('6200-6299.xml', 'classicPicks.xml', 'classicScrolls.xml'):
		path = os.path.join(DATA, 'xml', 'skills', f)
		if os.path.exists(path):
			out += re.findall(r'<skill id="(\d+)" levels="\d+" name="([^"]*)"', _read(path))
	return out


def quests():
	return sum(1 for f in os.listdir(os.path.join(JAVA, 'scripting', 'quest')) if f.endswith('.java'))
