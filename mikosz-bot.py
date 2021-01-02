import discord
from discord.ext import tasks,commands
#import dictionary
from dictionary import *
from datetime import datetime
import time
import rumps
import asyncio

def readToken(name='token'):
    token = open(name, "r")
    t = token.readlines()
    token =[]
    for line in t:
        j = line.replace('\n','')
        token.append(j)
    return token
token = readToken()[0]

client = commands.Bot(command_prefix="=")

@client.event
async def on_ready():
	task.start(client)
	print("------------------")
	print(print(datetime.now()))
	print("siemaa eniu -- bot online")

@client.command()
async def siema(ctx):
	await ctx.send("**siema eniu** <:sebaSmile:786002869718614078>")

@client.command()
async def cthulhu(ctx):
	await ctx.send("https://youtu.be/1ZB8uw0nlfw")

@client.command()
async def spanish(ctx):
	sp, en = get_random_spanish_word()
	await ctx.send("esp: "+sp+" -> "+en)

@client.command()
async def polish(ctx):
	slowo_dnia, slowo_dnia_href  = get_slowo_dnia()
	pl_meaning = get_znaczenia_slowa(slowo_dnia_href)
	await ctx.send("pl: "+slowo_dnia+" -> "+pl_meaning)

@client.command()
async def english(ctx):
	word, pronon, partofspeech, definition  = get_slowo_dnia_eng()
	await ctx.send("eng: "+word+" "+pronon+","+partofspeech+" -> "+definition)

@client.command()
async def knopers(ctx):
	await ctx.send('https://youtu.be/ZqAAjoeu0m4')
	

@client.command()
async def wotd(ctx):
	#esp
	sp, en = get_random_spanish_word()

	#pl
	slowo_dnia, slowo_dnia_href  = get_slowo_dnia()
	pl_meaning = get_znaczenia_slowa(slowo_dnia_href)

	#eng
	word, pronon, partofspeech, definition  = get_slowo_dnia_eng()
	
	await ctx.send("esp: "+sp+" -> "+en)
	await ctx.send("pl: "+slowo_dnia+" -> "+pl_meaning)
	await ctx.send("eng: "+word+" "+pronon+","+partofspeech+" -> "+definition)

send_time='21:37'
#message = "**word of the day:** <:figiSzlug:788156799114412052>"

@tasks.loop(seconds=31.0)
async def task(self):
	if(datetime.strftime(datetime.now(),'%H:%M') == send_time):
		#print(message)
		channel = client.get_channel(787624976521756673)
		#await channel.send(message)

		sp, en = get_random_spanish_word()
		slowo_dnia, slowo_dnia_href  = get_slowo_dnia()
		pl_meaning = get_znaczenia_slowa(slowo_dnia_href)
		word, pronon, partofspeech, definition  = get_slowo_dnia_eng()
		print(datetime.now())
		print("esp: "+sp+" -> "+en)
		print("pl: "+slowo_dnia+" -> "+pl_meaning)
		print("eng: "+word+" "+pronon+","+partofspeech+" -> "+definition)
		await channel.send("esp: "+sp+" -> "+en)
		await channel.send("pl: "+slowo_dnia+" -> "+pl_meaning)
		await channel.send("eng: "+word+" "+pronon+","+partofspeech+" -> "+definition)
		time.sleep(61.0)

client.run(token)


# Python 3.7+
#asyncio.run(main())

# macos menu icon
# class App(object):
#     def __init__(self):
#         self.app = rumps.App("Mikosz-bot", "🍅")

#     def run(self):
#         self.app.run()



# if __name__ == '__main__':
#     app = App()
#     asyncio.run(client.run(token))
#     app.run()

#

# run with
# nohup python3 -u /Users/mikolaj/Projects/word-of-the-day/mikosz-bot.py &

# stop with
# ps ax | grep mikosz-bot.py
# kill -9 [id]







