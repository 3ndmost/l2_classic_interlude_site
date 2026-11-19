"""Packet-by-packet audit of the protocol 110 layer, both directions, read from the server code and the client's opcode
tables (tools/re/data/*.json, extracted from the client's Engine.dll).

  python audit.py            prints a summary and the rows that need a look

Server -> client: every aCis server packet, how it reaches protocol 110 (translated to a Classic class, allowed through,
switching its own layout, replaced, or not sent), the opcode written on 110, and the client's own name for the handler
at that opcode; a name that does not resemble the packet's is flagged for a look (the client tables are complete and
were read from the client's handler tables).
Client -> server: every D0 request of the client's send code, routed or not; an unrouted one is "modern" (a Classic
system Interlude does not have, by name) or "check" (could be an Interlude feature: look at it by hand).
"""
import json
import os
import re

import extras

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OPCODES = os.path.join(ROOT, 'tools', 're', 'data')
NET = os.path.join(extras.JAVA, 'network')
SP = os.path.join(NET, 'serverpackets')

# Client requests of Classic systems Interlude never had (matched on the request's name).
MODERN = re.compile(r'BR_|Commission|CuriousHouse|Shape_Shifting|Ability|Alchemy|Vip|Lucky|Mentor|Arena|MatchGroup|PledgeBonus|'
	r'PledgeRecruit|PledgeWaiting|PledgeDraft|PledgeSignIn|PledgeJoinSys|Dominion|Cleft|BlockGame|CrataeCube|Fortress|ItemAuction|'
	r'BidItemAuction|Ensoul|NewEnchant|CardReward|Training|Beauty|XMas|Kalie|Balthus|SSOAuthn|RaidServer|MonsterBook|FlyMove|Awaken|'
	r'2ndPassword|Statistics|WebSession|Campaign|ResetShop|GoodsInventory|FirstPlayStart|ChangeAttribute|InzoneParty|PVPMatchRecord|'
	r'Mpcc|EventMatch|MiniGame|BookMarkSlot|UserBanInfo|NetPing|CallToChangeClass|PremiumItem|AddEnchantScroll|AccountAttendance', re.I)


def norm(name):
	n = name.lower()
	for cut in ('packet', 'classic'):
		n = n.replace(cut, '')
	n = re.sub(r'^ex', '', n)
	return re.sub(r'[^a-z0-9]', '', n)


def similar(a, b):
	a, b = norm(a), norm(b)
	if not a or not b:
		return False
	return a == b or a in b or b in a or (len(a) > 6 and a[:7] == b[:7])


def read(path):
	return open(path, encoding='utf-8', errors='replace').read()


def num(text):
	text = text.strip()
	try:
		return int(text, 16) if text.lower().startswith('0x') else int(text)
	except ValueError:
		return None


def pick(expr):
	"""The value a write takes on protocol 110: 'classic ? A : B' / 'CLIENT_PROTOCOL == CLASSIC_INTERLUDE ? A : B'."""
	expr = expr.strip()
	m = re.match(r'\(?(.+?)\)?\s*\?\s*([^:]+):\s*(.+)$', expr)
	if m:
		cond, a, b = m.groups()
		classic = 'classic' in cond.lower()
		negated = '!=' in cond or cond.strip().startswith('!')
		return num(b.strip(' )') if (classic and negated) else a.strip(' )')) if classic else None
	return num(expr.strip(' )'))


def opcode(cls, seen=None):
	"""('ord', n) / ('ext', n) / None: the first opcode the class writes on protocol 110."""
	path = os.path.join(SP, cls + '.java')
	if not os.path.exists(path):
		return None
	src = read(path)
	body = src[src.find('writeImpl'):] if 'writeImpl' in src else ''
	# A Classic layout kept in its own method (writeClassic and the like) comes first.
	method = re.search(r'private\s+void\s+(write\w*Classic\w*)\s*\(\s*\)\s*\{', src)
	if method and method.group(1) + '()' in body:
		body = src[method.end():] + body
	# An if (CLASSIC) { ... } block first, then plain writes.
	block = re.search(r'if\s*\(\s*Config\.CLIENT_PROTOCOL\s*==\s*ClientProtocol\.CLASSIC_INTERLUDE\s*\)\s*\{(.*?)\}', body, re.S)
	# The writes before a Classic if block, then the block's own (the opcode may be written before it, or in it).
	scan = body[:block.start()] + block.group(1) if block else body
	writes = re.findall(r'write([CH])\((.+?)\);', scan)
	if not writes:
		parent = re.search(r'extends\s+(\w+)', src)
		if parent and parent.group(1) != 'L2GameServerPacket' and parent.group(1) != (seen or ''):
			return opcode(parent.group(1), cls)
		return None
	kind, expr = writes[0]
	first = pick(expr)
	if kind != 'C' or first is None:
		return None
	if first == 0xFE and len(writes) > 1 and writes[1][0] == 'H':
		sub = pick(writes[1][1])
		return ('ext', sub) if sub is not None else None
	return ('ord', first)


# Rows read by hand: the opcode comes from a constructor argument or a parent class (checked 2026-11-16 against the
# client's handler names: all match).
VERIFIED = {
	'TradeOwnAdd': ('ord', 0x1A, 'ClassicTradeAdd(own)'), 'TradeOtherAdd': ('ord', 0x1B, 'ClassicTradeAdd(other)'),
	'TradePressOwnOk': ('ord', 0x53, 'ClassicTradeSignal(0x53)'), 'TradePressOtherOk': ('ord', 0x82, 'ClassicTradeSignal(0x82)'),
	'SendTradeDone': ('ord', 0x1C, 'ClassicTradeSignal(0x1C)'), 'PetInventoryUpdate': ('ord', 0xB4, 'AbstractInventoryUpdate, pet'),
}
# Client handlers present in Engine.dll's ordinary table but missing from the name table (pe.py Engine handler <op>).
UNNAMED = {0x48: 'MagicSkillUse', 0x49: 'MagicSkillCanceled', 0x55: 'FriendAddRequestResult', 0x59: 'FriendStatus',
	0x83: 'FriendAddRequest', 0xA0: 'PrivateStoreManageListSell', 0xA1: 'PrivateStoreListSell', 0xA2: 'PrivateStoreMsgSell',
	0xBD: 'PrivateStoreManageListBuy', 0xBE: 'PrivateStoreListBuy', 0xBF: 'PrivateStoreMsgBuy', 0xDD: 'RecipeItemMakeInfo',
	0xE0: 'RecipeShopItemInfo', 0x00: 'Die'}


# The client's name for the same packet (each checked by hand 2026-11-16: the handler is the matching one).
SYNONYMS = {'AcquireSkillList', 'AllyCrest', 'BuyList', 'CharCreateFail', 'CharCreateOk', 'CharDeleteFail', 'CharDeleteOk',
	'CharSelectInfo', 'CharSelected', 'ClanHallDecoration', 'CreatureSay', 'ExConfirmCancelItem', 'ExConfirmVariationGemstone',
	'ExConfirmVariationItem', 'ExConfirmVariationRefiner', 'HennaItemUnequipInfo', 'LeaveWorld', 'MoveToLocation', 'NpcSay',
	'PartyMatchDetail', 'PartyMatchList', 'PetInfo', 'ServerClose', 'StopRotation', 'TitleUpdate', 'TradeItemUpdate',
	'TutorialShowQuestionMark', 'UserInfo'}


def server_side():
	client = read(os.path.join(NET, 'GameClient.java'))
	lines = client.splitlines()
	translate = {}
	for i, line in enumerate(lines):
		if 'allowed =' in line:
			continue
		for name in re.findall(r'instanceof\s+(\w+)', line):
			for nxt in lines[i:i + 16]:
				m = re.search(r'new\s+(Classic\w+)\(', nxt) or re.search(r'(Classic\w+)\.STATIC_PACKET', nxt)
				if m:
					translate.setdefault(name, m.group(1))
					break
				if nxt is not line and 'instanceof' in nxt:
					break
	allowed = set(re.findall(r'instanceof\s+(\w+)', next((l for l in lines if 'allowed =' in l), '')))
	ord_t = {int(k): v for k, v in json.load(open(os.path.join(OPCODES, 'ord_opcodes.json'), encoding='utf-8')).items()}
	ext_t = {int(k): v for k, v in json.load(open(os.path.join(OPCODES, 'ext_opcodes.json'), encoding='utf-8')).items()}
	groups = extras.packets()
	group_of = {n: g for g, names in groups.items() for n in names}
	rows = []
	for name in sorted(group_of):
		group = group_of[name]
		sent, route = None, ''
		if name in translate:
			sent, route = translate[name], 'translated'
		elif 'CLASSIC_INTERLUDE' in read(os.path.join(SP, name + '.java')):
			sent, route = name, 'own switch'
		elif name in allowed:
			sent, route = name, 'allowed as is'
		elif group == 'Classic replacement':
			cand = [f[:-5] for f in os.listdir(SP) if f.startswith('Classic') and norm(f[7:-5]) == norm(name)]
			sent, route = (cand[0] if cand else None), 'replacement'
		elif group == 'Connected':
			sent, route = name, 'connected'
		op = opcode(sent) if sent else None
		if name in VERIFIED:
			op = VERIFIED[name][:2]
		handler = (ord_t if op and op[0] == 'ord' else ext_t).get(op[1]) if op else None
		if op and op[0] == 'ord' and not handler and op[1] in UNNAMED:
			handler = UNNAMED[op[1]] + ' (handler present, unnamed in the table)'
		if not sent:
			check = 'not sent'
		elif not op:
			check = 'opcode not read'
		elif not handler:
			check = 'no client handler'
		elif similar(handler, name) or similar(handler, sent) or name in SYNONYMS:
			check = 'ok'
		else:
			check = 'name differs'
		opstr = ('FE:%04X' % op[1] if op[0] == 'ext' else '%02X' % op[1]) if op else ''
		rows.append({'packet': name, 'group': group, 'route': route, 'sent': sent or '', 'opcode': opstr, 'handler': (handler or '').replace('Packet', ''), 'check': check})
	return rows


# Unrouted client requests reviewed by hand (2026-11-16): why nothing is needed, or that it is open.
VERDICTS = {
	'RequestAllAgitInfo': ('open', 'clan halls in World Info > Region Info; waiting for a decision since 2026-10'),
	'RequestExTryToPutEnchantSupportItem': ('not needed', 'Interlude has no enchant support items; the slot stays empty'),
	'RequestTeleportBookMark': ('later chronicle', 'My Teleports bookmarks'),
	'RequestJump': ('later chronicle', 'jumping'),
	'RequestSeedPhase': ('later chronicle', 'Seed of Destruction'),
	'EndScenePlayer': ('not needed', 'for in-engine scenes (ExStartScenePlayer), which the server never starts; its full-screen movies (ExShowUsm) need no reply'),
	'RequestExEscapeScene': ('not needed', 'for in-engine scenes (ExStartScenePlayer), which the server never starts; its full-screen movies (ExShowUsm) need no reply'),
	'RequestShowAgitSiegeInfo': ('not needed', 'answered with RequestAllCastleInfo (tested 2026-09-30)'),
	'RequestBuySellUIClose': ('not needed', 'only says a shop window closed; aCis keeps no state for it'),
	'RequestCrystallizeItemCancel': ('not needed', 'only says the crystallize window closed'),
	'RequestShowNewUserPetition': ('minor', 'petition window extra; petitions work'),
	'ResponsePetitionAlarm': ('minor', 'petition window extra; petitions work'),
}
AGIT_UI = re.compile(r'Agit(Bid|Lot|Registering|ForBid|DetailInfo|State|Initialize)|RegisteringAgit', re.I)


def client_side():
	c2s = json.load(open(os.path.join(OPCODES, 'c2s_opcodes.json'), encoding='utf-8'))
	lines = read(os.path.join(NET, 'GamePacketHandler.java')).splitlines()
	start = next(i for i, l in enumerate(lines) if 'subOpcode = buf.getShort()' in l and i > 300)
	end = next(i for i, l in enumerate(lines) if "Do not pass a Classic extended packet" in l)
	seg = '\n'.join(lines[start:end])
	routed = {}
	for m in re.finditer(r'case\s+((?:0x[0-9A-Fa-f]+\s*,?\s*)+):|subOpcode\s*==\s*0x([0-9A-Fa-f]+)', seg):
		values = re.findall(r'0x([0-9A-Fa-f]+)', m.group(1)) if m.group(1) else [m.group(2)]
		target = re.search(r'new\s+(\w+)\(', seg[m.end():m.end() + 400])
		for v in values:
			routed.setdefault(int(v, 16), target.group(1) if target else '')
	# The client table's sub-opcodes are wrong for a few requests (the manor's four sit at 0x01-0x04, not 0xD0); a request
	# whose class is created anywhere in the handler (any connection state) counts as routed, under its name.
	created = set(re.findall(r'new\s+(\w+)\(', '\n'.join(lines)))
	for m in re.finditer(r'subOpcode\s*>=\s*0x([0-9A-Fa-f]+)\s*&&\s*subOpcode\s*<=\s*0x([0-9A-Fa-f]+)', seg):
		target = re.search(r'new\s+(\w+)\(', seg[m.end():m.end() + 300])
		for k in range(int(m.group(1), 16), int(m.group(2), 16) + 1):
			routed.setdefault(k, target.group(1) if target else '')
	rows = []
	for key, fmt in c2s.items():
		sub, name = key.split('|')
		if not fmt.startswith('ch'):
			continue
		sub = int(sub)
		if sub in routed:
			state = 'routed'
		elif name in created:
			state = 'routed'
			routed[sub] = name + ' (by name)'
		elif MODERN.search(name):
			state = 'modern'
		elif name in VERDICTS:
			state = VERDICTS[name][0]
		elif AGIT_UI.search(name):
			state = 'not needed'
		else:
			state = 'check'
		note = VERDICTS[name][1] if name in VERDICTS else ('Classic clan hall auction window; Interlude auctions use NPC pages (tested)' if AGIT_UI.search(name) and state == 'not needed' else '')
		rows.append({'opcode': 'D0:%04X' % sub, 'request': name, 'format': fmt, 'state': state, 'handler': routed.get(sub, ''), 'note': note})
	rows.sort(key=lambda r: r['opcode'])
	return rows


if __name__ == '__main__':
	s = server_side()
	c = client_side()
	from collections import Counter
	print('server packets:', len(s), Counter(r['check'] for r in s))
	for r in s:
		if r['check'] not in ('ok', 'not sent'):
			print('  S', r['packet'], r['route'], r['sent'], r['opcode'], r['handler'], '->', r['check'])
	print('client D0 requests:', len(c), Counter(r['state'] for r in c))
	for r in c:
		if r['state'] == 'check':
			print('  C', r['opcode'], r['request'], r['format'])
