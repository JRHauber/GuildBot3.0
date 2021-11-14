import discord
import logging
from discord.ext import commands
import random
import json
import os
from dotenv import load_dotenv
import numpy as np
from json import JSONEncoder
from os import getenv

global characterList
global selectedList
global selectedChars
global initiativeList1
global initiativeList2
global initiativeList3
global initiativeList4
global initiativeListS
global tokenList
global rankDice
global rankAdder
global rankHealth
load_dotenv("D:/Dev/Python/Discord_Bot/.env")

bot_token = getenv("TOKEN")
characterList = []
selectedList = {}
selectedChars = []
initiativeList1 = []
initiativeList2 = []
initiativeList3 = []
initiativeList4 = []
initiativeListS = []
tokenList = []

rankDice = {
	'acolyte': 20,
	'rank1': 20,
	'apprentice': 25,
	'rank2': 25,
	'lord': 30,
	'rank3': 30,
	'highlord': 30,
	'rank4': 30,
	'darth': 35,
	'rank5': 35,
	'idl': 35,
	'rank6': 35,
	'council': 45,
	'chosen': 50,
	'emperor': 50
}
rankAdder = {
	'acolyte': 0,
	'rank1': 0,
	'apprentice': 0,
	'rank2': 0,
	'lord': 3,
	'rank3': 3,
	'highlord': 5,
	'rank4': 5,
	'darth': 6,
	'rank5': 6,
	'idl': 10,
	'rank6': 10,
	'council': 20,
	'chosen': 25,
	'emperor': 27
}
rankHealth = {
	'acolyte': 2,
	'rank1': 2,
	'apprentice': 3,
	'rank2': 3,
	'lord': 4,
	'rank3': 4,
	'highlord': 4,
	'rank4': 4,
	'darth': 5,
	'rank5': 5,
	'idl': 5,
	'rank6': 5,
	'council': 7,
	'chosen': 8,
	'emperor': 9
}

for x in range(1, 10000):
	selectedList[x] = 0


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

activity = discord.Game("!gbothelp")
bot = commands.Bot(activity=activity, command_prefix='!g')

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

class character:
	def __init__(self, name, uID, dice, adder, health, maxhealth, cID):
		self.name = name
		self.uID = uID
		self.dice = dice
		self.adder = adder
		self.health = health
		self.maxhealth = maxhealth
		self.cID = cID


class selectedClass:
	def __init__(self, uID, cID):
		self.uID = uID
		self.cID = cID

class token:
	def __init__(self,name,dice,adder,health,creator):
		self.name = name
		self.dice = dice
		self.adder = adder
		self.health = health
		self.maxhealth = maxhealth
		self.uID = creator

class charEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

def rollDice(dMax = 1, mod = 0, dNum = 1, name = ""):
	dRes = ""
	dRes += name.lower().title() + "\'s roll"
	if(dNum > 1):
		sum = 0
		dRes += "s: `["
		for x in range(0, dNum):
			result = int(np.floor(random.uniform(1, int(dMax)+1)))
			result += int(mod)
			result2 = str(result)
			sum += result
			if(result == int(dMax) + int(mod)):
				result2 += " - CRIT"
			if(x < dNum):
				dRes += result2 + ", "
		dRes = dRes[:-2]
		dRes += "]` Total: `" + str(sum) + "`"
	else:
		dRes += " `["
		result = int(np.floor(random.uniform(1, int(dMax)+1)))
		result += int(mod)
		result2 = str(result)
		if(result == int(dMax) + int(mod)):
			result2 += " - CRIT"
		dRes += result2 + "]`"
	return dRes

def titleString(str):
	return str.capitalize()

path = 'D:/Dev/Python/Discord_Bot/'

def fReload():
	global characterList
	global selectedChars
	characterList.clear()
	selectedChars.clear()
	f = open(path + 'characters.json', 'r')
	data = f.read()
	characterList = json.loads(data)
	f = open(path + 'selected.json', 'r')
	data = f.read()
	selectedChars = json.loads(data)

def writeTable(tbl, fileName):
	with open(path + fileName + '.json', 'w') as outfile:
		json.dump(tbl, outfile, cls=charEncoder)
	fReload()

def generateCID():
	cID = 0
	cID = random.randrange(1,9999)
	i = 0
	while (i < len(characterList)) or (i != 123456):
		if (cID == characterList[i]['cID']):
			i = 0
			cID = random.randrange(1,9999)
		else:
			i = 123456
			return cID

def handleSelect(uID, cID):
	selectedList[cID] = uID
	newSelect = selectedClass(uID, cID)
	selectedChars.append(newSelect)
	writeTable(selectedChars, 'selected')

def loadSelected():
	for x in selectedChars:
		selectedList[x['cID']] = x['uID']

def findSelected(uID):
	found = 0
	for x in selectedList:
		if(int(selectedList[x]) == int(uID)):
			found = 1
			return x
	if(found == 0):
		return 0

def findCharacter(cID):
	for x in characterList:
		if(x['cID'] == cID):
			return characterList.index(x)

def clearSelected(uID):
	for x in selectedList:
		if(selectedList[x] == uID):
			selectedList[x] = 0

	selectedChars.clear()


f = open(path + 'characters.json', 'r')
data = f.read()
characterList = json.loads(data)

f = open(path + 'selected.json', 'r')
data = f.read()
selectedChars = json.loads(data)
loadSelected()

f = open(path + 'initiative.json', 'r')
data = f.read()
initiativeList = json.loads(data)

@bot.command()
async def test(ctx, *args):
	await ctx.send('{}'.format(' '.join(args)))

@bot.command()
async def bothelp(ctx):
	await ctx.send('Read the wiki if you have any questions! https://github.com/Lanidae/GuildBot3.0/wiki')
@bot.command()
async def add(ctx, arg1, arg2):
	adder = rankAdder[arg2.lower()]
	dice = rankDice[arg2.lower()]
	health = rankHealth[arg2.lower()]
	newChar = character(arg1, ctx.author.id, dice, adder, health, health, generateCID())
	characterList.append(newChar)
	writeTable(characterList, 'characters')
	logging.warning(characterList)
	await ctx.send('Added! You are: ' + arg1 + ' and your dice is d' + str(dice) + '+' + str(adder) + ' and you have ' + str(health) + ' health')

@bot.command()
async def t(ctx, arg):
	await ctx.send(selectedList[int(arg)])

@bot.command()
async def select(ctx, arg):
	arg = arg or ''
	clearSelected(ctx.author.id)
	
	for x in characterList:
		#await ctx.send(x)
		if (x['name'].lower() == arg.lower()):
			if (x['uID'] == ctx.author.id):
				handleSelect(ctx.author.id, x['cID'])
				await ctx.send('You selected - `' + titleString(arg) + '` - I\'ll use them until you tell me to use someone else :)')
				break
			else:
				await ctx.send('Sorry, you can only select your own characters!')
				break
	if(findSelected(ctx.author.id) == 0):
		await ctx.send('Sorry, I can\'t find a character with that name!')

@bot.command()
async def update(ctx, arg1):
	scid = findSelected(ctx.author.id)
	i = 0
	while(i < len(characterList)):
		if(characterList[i]['cID'] == scid):
			characterList[i]['health'] = rankHealth[arg1.lower()]
			characterList[i]['maxhealth'] = rankHealth[arg1.lower()]
			characterList[i]['dice'] = rankDice[arg1.lower()]	
			characterList[i]['adder'] = rankAdder[arg1.lower()]
			i = 100000000
			break
		i = i + 1
	writeTable(characterList, 'characters')
	await ctx.send('You\'ve been upgraded to ' + titleString(arg1))

@bot.command()
async def roll(ctx, *args):
	if(len(args) == 0):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can roll your rank dice.")
		else:
			localchar = characterList[findCharacter(findSelected(ctx.author.id))]
			dice = localchar['dice']
			adder = localchar['adder']
			count = 1
			await ctx.send(rollDice(dice, adder, count, localchar['name']))
	else:

		temp = {}
		if '+' not in args[0]:
			if 'd' not in args[0]:
				await ctx.send(rollDice(int(args[0]), 0, 1, ctx.author.display_name))
			else:
				temp = args[0].split('d')
				if temp[0] != '':
					await ctx.send(rollDice(int(temp[1]), 0, int(temp[0]), ctx.author.display_name))
				else:
					await ctx.send(rollDice(int(temp[1]), 0, 1, ctx.author.display_name))
		else:
			if 'd' not in args[0]:
				temp = args[0].split('+')
				await ctx.send(rollDice(int(temp[0]), int(temp[1]), 1, ctx.author.display_name))
			else:
				temp = args[0].split('d')
				if temp[0] != '':
					count = temp[0]
				else:
					count = 1
				temp = temp[1].split('+')
				await ctx.send(rollDice(int(temp[0]), int(temp[1]), int(count), ctx.author.display_name))

@bot.command()
async def heal(ctx, *args):
	if(len(args) == 0):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can heal you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if (1 + int(characterList[cPos]['health'])) > int(characterList[cPos]['maxhealth']):
				characterList[cPos]['health'] = characterList[cPos]['maxhealth']
				writeTable(characterList, 'characters')
				await ctx.send("You tried healing over max health, so I just set you to full health. You're welcome")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) + 1
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))
 
	else:
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can heal you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if (int(args[0]) + int(characterList[cPos]['health'])) > int(characterList[cPos]['maxhealth']):
				characterList[cPos]['health'] = characterList[cPos]['maxhealth']
				writeTable(characterList, 'characters')
				await ctx.send("You tried healing over max health, so I just set you to full health. You're welcome")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) + int(args[0])
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))


@bot.command()
async def h(ctx, *args):
	if(len(args) == 0):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can heal you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if (1 + int(characterList[cPos]['health'])) > int(characterList[cPos]['maxhealth']):
				characterList[cPos]['health'] = characterList[cPos]['maxhealth']
				writeTable(characterList, 'characters')
				await ctx.send("You tried healing over max health, so I just set you to full health. You're welcome")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) + 1
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))
 
	else:
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can heal you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if (int(args[0]) + int(characterList[cPos]['health'])) > int(characterList[cPos]['maxhealth']):
				characterList[cPos]['health'] = characterList[cPos]['maxhealth']
				writeTable(characterList, 'characters')
				await ctx.send("You tried healing over max health, so I just set you to full health. You're welcome")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) + int(args[0])
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))

@bot.command()
async def d(ctx, *args):
	if(len(args) == 0):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can damage you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if ((int(characterList[cPos]['health']) - 1) <= 0) or ((int(characterList[cPos]['health']) - 1) <= -1):
				characterList[cPos]['health'] = (int(characterList[cPos]['health']) - 1)
				writeTable(characterList, 'characters')
				await ctx.send("Uh-Oh, you're at sub 0 health. If you don't have Force Body or Endurance, you're out of the fight")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) - 1
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))
	else:
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can damage you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if ((int(characterList[cPos]['health']) - int(args[0])) <= 0) or ((int(characterList[cPos]['health']) - int(args[0])) <= -1):
				characterList[cPos]['health'] = (int(characterList[cPos]['health']) - 1)
				writeTable(characterList, 'characters')
				await ctx.send("Uh-Oh, you're at sub 0 health. If you don't have Force Body or Endurance, you're out of the fight")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) - int(args[0])
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))

@bot.command()
async def damage(ctx, *args):
	if(len(args) == 0):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can damage you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if ((int(characterList[cPos]['health']) - 1) <= 0) or ((int(characterList[cPos]['health']) - 1) <= -1):
				characterList[cPos]['health'] = (int(characterList[cPos]['health']) - 1)
				writeTable(characterList, 'characters')
				await ctx.send("Uh-Oh, you're at sub 0 health. If you don't have Force Body or Endurance, you're out of the fight")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) - 1
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))
	else:
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can damage you.")
		else:
			cPos = findCharacter(findSelected(ctx.author.id))
			if ((int(characterList[cPos]['health']) - int(args[0])) <= 0) or ((int(characterList[cPos]['health']) - int(args[0])) <= -1):
				characterList[cPos]['health'] = (int(characterList[cPos]['health']) - 1)
				writeTable(characterList, 'characters')
				await ctx.send("Uh-Oh, you're at sub 0 health. If you don't have Force Body or Endurance, you're out of the fight")
			else:
				characterList[cPos]['health'] = int(characterList[cPos]['health']) - int(args[0])
				writeTable(characterList, 'characters')
				await ctx.send("Set your health to: " + str(characterList[cPos]['health']))


@bot.command()
async def report(ctx):
	if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can give you a character report.")
	else:
		cPos = findCharacter(findSelected(ctx.author.id))
		message = '```\nName: ' + characterList[cPos]['name'] + '\nHealth: ' + str(characterList[cPos]['health']) + '/' + str(characterList[cPos]['maxhealth']) + '\nDice: d' + str(characterList[cPos]['dice']) + '+' + str(characterList[cPos]['adder']) + '```'
		await (ctx.send(message))


@bot.command()
async def init(ctx, *args):
	global initiativeList1
	global initiativeList2
	global initiativeList3
	global initiativeList4
	global initiativeListS
	if (args[0] == 'add'):
		if(findSelected(ctx.author.id) == 0):
			await ctx.send("I'm sorry, it doesn't look like you've selected a character yet. Be sure to do !gselect <name> so I can add you to initiative")
		else:
			if (args[1] == '1'):
				initiativeList1.append(findSelected(ctx.author.id))
				writeTable(initiativeList1, 'initiative1')
				await ctx.send("I added you to the initiative list for Squad 1!")
			elif (args[1] == '2'):
				initiativeList2.append(findSelected(ctx.author.id))
				writeTable(initiativeList2, 'initiative2')
				await ctx.send("I added you to the initiative list for Squad 2!")
			elif (args[1] == '3'):
				initiativeList3.append(findSelected(ctx.author.id))
				writeTable(initiativeList3, 'initiative3')
				await ctx.send("I added you to the initiative list for Squad 3!")
			elif (args[1] == '4'):
				initiativeList4.append(findSelected(ctx.author.id))
				writeTable(initiativeList4, 'initiative4')
				await ctx.send("I added you to the initiative list for Squad 4!")
			elif (args[1].upper() == 'S'):
				initiativeListS.append(findSelected(ctx.author.id))
				writeTable(initiativeListS, 'initiativeS')
				await ctx.send("I added you to the initiative list for Squad sneaky!")
	elif (args[0] == 'scramble'):
		if (args[1] == '1'):
			random.shuffle(initiativeList1)
			writeTable(initiativeList1, 'initiative1')
			await ctx.send("Initiative list for Squad 1 has been randomized! No need to roll")
		elif (args[1] == '2'):
			random.shuffle(initiativeList2)
			writeTable(initiativeList2, 'initiative2')
			await ctx.send("Initiative list for Squad 2 has been randomized! No need to roll")
		elif (args[1] == '3'):
			random.shuffle(initiativeList3)
			writeTable(initiativeList3, 'initiative3')
			await ctx.send("Initiative list for Squad 3 has been randomized! No need to roll")
		elif (args[1] == '4'):
			random.shuffle(initiativeList4)
			writeTable(initiativeList4, 'initiative4')
			await ctx.send("Initiative list for Squad 4 has been randomized! No need to roll")
		elif (args[1].upper() == 'S'):
			random.shuffle(initiativeListS)
			writeTable(initiativeListS, 'initiativeS')
			await ctx.send("Initiative list for Squad Sneaky has been randomized! No need to roll")
	elif (args[0] == 'clear'):
		if (args[1] == '1'):
			initiativeList1.clear()
			writeTable(initiativeList1, 'initiative1')
			await ctx.send("Initiative cleared for Squad 1, ready for the next event!")
		elif (args[1] == '2'):
			initiativeList2.clear()
			writeTable(initiativeList2, 'initiative2')
			await ctx.send("Initiative cleared for Squad 2, ready for the next event!")
		elif (args[1] == '3'):
			initiativeList3.clear()
			writeTable(initiativeList3, 'initiative3')
			await ctx.send("Initiative cleared for Squad 3, ready for the next event!")
		elif (args[1] == '4'):
			initiativeList4.clear()
			writeTable(initiativeList4, 'initiative4')
			await ctx.send("Initiative cleared for Squad 4, ready for the next event!")
		elif (args[1].upper() == 'S'):
			initiativeList1.clear()
			writeTable(initiativeListS, 'initiativeS')
			await ctx.send("Initiative cleared for Squad Sneaky, ready for the next event!")
	elif (args[0] == 'print'):
		if (args[1] == '1'):
			output = "```\n"
			for x in range(len(initiativeList1)):
				cPos = findCharacter(initiativeList1[x])
				output += str(x+1) + " - " + characterList[cPos]['name'] + " - " + str(characterList[cPos]['health']) + "/" + str(characterList[cPos]['maxhealth']) + "\n"
			output += "```"
			await ctx.send("Here's that list for Squad 1!\n" + output)
		elif (args[1] == '2'):
			output = "```\n"
			for x in range(len(initiativeList2)):
				cPos = findCharacter(initiativeList2[x])
				output += str(x+1) + " - " + characterList[cPos]['name'] + " - " + str(characterList[cPos]['health']) + "/" + str(characterList[cPos]['maxhealth']) + "\n"
			output += "```"
			await ctx.send("Here's that list for Squad 2!\n" + output)
		elif (args[1] == '3'):
			output = "```\n"
			for x in range(len(initiativeList3)):
				cPos = findCharacter(initiativeList3[x])
				output += str(x+1) + " - " + characterList[cPos]['name'] + " - " + str(characterList[cPos]['health']) + "/" + str(characterList[cPos]['maxhealth']) + "\n"
			output += "```"
			await ctx.send("Here's that list for Squad 3!\n" + output)
		elif (args[1] == '4'):
			output = "```\n"
			for x in range(len(initiativeList4)):
				cPos = findCharacter(initiativeList4[x])
				output += str(x+1) + " - " + characterList[cPos]['name'] + " - " + str(characterList[cPos]['health']) + "/" + str(characterList[cPos]['maxhealth']) + "\n"
			output += "```"
			await ctx.send("Here's that list for Squad 4!\n" + output)
		elif (args[1].upper() == 'S'):	
			output = "```\n"
			for x in range(len(initiativeListS)):
				cPos = findCharacter(initiativeListS[x])
				output += str(x+1) + " - " + characterList[cPos]['name'] + " - " + str(characterList[cPos]['health']) + "/" + str(characterList[cPos]['maxhealth']) + "\n"
			output += "```"
			await ctx.send("Here's that list for Squad Sneaky!\n" + output)	
	elif (args[0] == 'start'):
		if (args[1] == '1'):
			cPos = findCharacter(initiativeList1[0])
			uID = str(characterList[cPos]['uID'])
			initiativeList1.append(initiativeList1.pop(0))
			await ctx.send(f'<@{uID}> you\'re up first! Lucky you! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '2'):
			cPos = findCharacter(initiativeList2[0])
			uID = str(characterList[cPos]['uID'])
			initiativeList2.append(initiativeList2.pop(0))
			await ctx.send(f'<@{uID}> you\'re up first! Lucky you! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '3'):
			cPos = findCharacter(initiativeList3[0])
			uID = str(characterList[cPos]['uID'])
			initiativeList3.append(initiativeList3.pop(0))
			await ctx.send(f'<@{uID}> you\'re up first! Lucky you! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '4'):
			cPos = findCharacter(initiativeList4[0])
			uID = str(characterList[cPos]['uID'])
			initiativeList4.append(initiativeList4.pop(0))
			await ctx.send(f'<@{uID}> you\'re up first! Lucky you! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1].upper() == 'S'):
			cPos = findCharacter(initiativeListS[0])
			uID = str(characterList[cPos]['uID'])
			initiativeListS.append(initiativeListS.pop(0))
			await ctx.send(f'<@{uID}> you\'re up first! Lucky you! You\'re playing as ' + characterList[cPos]['name'])
	elif (args[0] == 'next'):
		if (args[1] == '1'):
			cPos = findCharacter(initiativeList1[0])
			uID = characterList[cPos]['uID']
			initiativeList1.append(initiativeList1.pop(0))
			await ctx.send(f'<@{uID}> it\'s your turn! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '2'):
			cPos = findCharacter(initiativeList2[0])
			uID = characterList[cPos]['uID']
			initiativeList2.append(initiativeList2.pop(0))
			await ctx.send(f'<@{uID}> it\'s your turn! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '3'):
			cPos = findCharacter(initiativeList3[0])
			uID = characterList[cPos]['uID']
			initiativeList3.append(initiativeList3.pop(0))
			await ctx.send(f'<@{uID}> it\'s your turn! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1] == '4'):
			cPos = findCharacter(initiativeList4[0])
			uID = characterList[cPos]['uID']
			initiativeList4.append(initiativeList4.pop(0))
			await ctx.send(f'<@{uID}> it\'s your turn! You\'re playing as ' + characterList[cPos]['name'])
		elif (args[1].upper() == 'S'):
			cPos = findCharacter(initiativeListS[0])
			uID = characterList[cPos]['uID']
			initiativeListS.append(initiativeListS.pop(0))
			await ctx.send(f'<@{uID}> it\'s your turn! You\'re playing as ' + characterList[cPos]['name'])
	elif (args[0] == 'remove'):
		name = args[2].lower()
		role = discord.utils.find(lambda r: r.name == "Event Runner", ctx.message.guild.roles)
		if role in ctx.author.roles:
			if(args[1] == '1'):
			 i = 0
			 while(i < len(initiativeList1)):
			 	cpos = findCharacter(initiativeList1[i])
			 	if(name == characterList[cpos]['name'].lower()):
			 		initiativeList1.remove(characterList[cpos]['cID'])
			 		i = 10000000
			 		break
			 	i = i + 1
			elif(args[1] == '2'):
				i = 0
				while(i < len(initiativeList2)):
			 		cpos = findCharacter(initiativeList2[i])
			 		if(name == characterList[cpos]['name'].lower()):
			 			initiativeList2.remove(characterList[cpos]['cID'])
			 			i = 10000000
			 			break
			 		i = i + 1
			elif(args[1] == '3'):
				i = 0
				while(i < len(initiativeList3)):
			 		cpos = findCharacter(initiativeList3[i])
			 		if(name == characterList[cpos]['name'].lower()):
			 			initiativeList3.remove(characterList[cpos]['cID'])
			 			i = 10000000
			 			break
			 		i = i + 1
			elif(args[1] == '4'):
				i = 0
				while(i < len(initiativeList4)):
			 		cpos = findCharacter(initiativeList4[i])
			 		if(name == characterList[cpos]['name'].lower()):
			 			initiativeList4.remove(characterList[cpos]['cID'])
			 			i = 10000000
			 			break
			 		i = i + 1
			elif(args[1] == 'S'):
				i = 0
				while(i < len(initiativeListS)):
			 		cpos = findCharacter(initiativeListS[i])
			 		if(name == characterList[cpos]['name'].lower()):
			 			initiativeListS.remove(characterList[cpos]['cID'])
			 			i = 10000000
			 			break
			 		i = i + 1
			await ctx.send(titleString(name) + " has been removed from initiative!")
		else:
			await ctx.send("You are not allowed to remove people from initiative! Rude!")


		
bot.run(bot_token)