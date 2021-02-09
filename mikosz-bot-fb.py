import asyncio
import fbchat
import random
from rap import *
import sys
import time

from os import listdir
from os.path import isfile, join
import collections

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime
import subprocess
import shlex


# If the script is running on Windows, change the default policy for the event loops to be compatible
# if os.name == "nt":
#     asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy


mypath = "/Users/mikolaj/Projects/mikosz-bot/emotki/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

names={}
for f in onlyfiles:
    if(f.split(".")[0]!=""):
        names[f.split(".")[0]] = 1
icons = collections.OrderedDict(sorted(names.items()))

def readToken(name='token'):
    token = open(name, "r")
    t = token.readlines()
    token =[]
    for line in t:
        j = line.replace('\n','')
        token.append(j)
    return token

token = readToken()
email = token[1]
password = token[2]
owm_token = token[3]

admins_id = {"100001354410639"} #moje id

def getRandomEmoteName():
    return random.choice(list(icons.keys()))

def getWeatherInfo(city="Krakow, PL"):
    owm = OWM(owm_token)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    # w.detailed_status         # 'clouds'
    # w.wind()                  # {'speed': 4.6, 'deg': 330}
    # w.humidity                # 87
    # w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    # w.rain                    # {}
    # w.heat_index              # None
    # w.clouds                  # 75
    return city,w

# Listen for new events and when that event is a new received message, reply to the author of the message
async def listen(listener, session):
    async for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
            # If you're not the author, echo
            try:
                if event.author.id != session.user.id:
                    for icon in icons.items():
                        if(event.message.text==":"+icon[0]+":"):
                            client = fbchat.Client(session=session)
                            with open(mypath+icon[0]+".png", "rb") as f:
                                files = await client.upload([("emote.png", f, "image/png")])
                            await event.thread.send_text(text=None, files=files)

                    if(event.message.text=="=emotes"):
                        keys="Available emotes:\n\n"
                        for icon in icons.keys():
                            keys+=":"+icon+":\n"
                        await event.thread.send_text(keys)

                    elif(event.message.text=="=randomemote"):
                        client = fbchat.Client(session=session)
                        e = getRandomEmoteName()
                        with open(mypath+e+".png", "rb") as f:
                            files = await client.upload([("emote.png", f, "image/png")])
                        await event.thread.send_text(text=":"+e+":", files=files)

                    elif(event.message.text=="=status"):
                        await event.thread.send_text("online 🤖")

                    elif(event.message.text=="=help"):
                        msg="Available commands:\n\n=help\n=emotes\n=randomemote\n=status\n=log [msg]\n=links\n=pogoda\n=rapuj [n-rhymes]"
                        await event.thread.send_text(msg)

                    elif(event.message.text.startswith("=log")):
                        msg = event.message.text.split("=log ")[1]
                        with open("logs.txt", "a") as f:
                            f.write("\n"+msg)
                        await event.thread.send_text("logged: "+msg)

                    elif(event.message.text=="=pogoda"):
                        city, w = getWeatherInfo()
                        temp = w.temperature('celsius') 
                        msg = "Pogoda dla "+city+":\n"+str(temp['temp'])+"°C (średnia),\n"+str(temp['feels_like'])+"°C (odczuwalna),\n details: "+ str(w.detailed_status)                     
                        await event.thread.send_text(msg)

                    elif(event.message.text.startswith("=links")):
                        await event.thread.send_text("https://thezapalsky.github.io/links/")

                    elif(event.message.text.startswith("==restart") and (event.author.id in admins_id)):
                        print("--restarting--")
                        await event.thread.send_text("--restarting--")
                        subprocess.call('./run.sh')

                    elif(event.message.text.startswith("nk ")):
                        await event.thread.send_text("https://youtu.be/aHtEm9sxzYg")

                    elif(event.message.text=="itzpp" or event.message.text=="i to za panstwowe pieniadze" or event.message.text=="i to za państwowe pieniądze"):
                        await event.thread.send_text("https://youtu.be/taFbS3abVdI")

                    elif(event.message.text.startswith("=rapuj")):
                        start = time.time()
                        try:
                            ile = event.message.text.split("=rapuj ")[1]
                            ile = int(ile)
                            if(ile>8):
                                ile=8
                            print(ile)
                            rap_lines = RapujMordo(ile)
                        except:
                            pass
                            print("error in parsing str->int")
                            rap_lines = RapujMordo()

                        #print(rap_lines)
                        for lists in rap_lines:
                            for l in lists:
                                await event.thread.send_text(l) 
                        end = time.time()
                        print(end - start)
                        
                    # if(event.message.text==":figiSzlug:"):
                    #     client = fbchat.Client(session=session)
                    #     with open("figiSzlug.png", "rb") as f:
                    #         files = await client.upload([("figiSzlug.png", f, "image/png")])
                    #     await event.thread.send_text(text=None, files=files)
                        #await event.thread.send_text(event.message.text)
            except:
                pass
                print("Unexpected error:", sys.exc_info()[0])

async def main():
    session = await fbchat.Session.login(email, password)

    client = fbchat.Client(session=session)
    listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

    listen_task = asyncio.create_task(listen(listener, session))

    client.sequence_id_callback = listener.set_sequence_id
    print("fb-bot online")
    print(datetime.now())
    # Call the fetch_threads API once to get the latest sequence ID
    await client.fetch_threads(limit=1).__anext__()

    # Let the listener run, otherwise the script will stop
    await listen_task
try:
    asyncio.run(main())
except:
    print("---END---")
    print(datetime.now())
    print("Unexpected error:", sys.exc_info()[0])
    print("---RESTARTING---")
    subprocess.call('./run.sh')