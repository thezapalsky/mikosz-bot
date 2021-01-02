import asyncio
import fbchat
import random


from os import listdir
from os.path import isfile, join
import collections

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# If the script is running on Windows, change the default policy for the event loops to be compatible
# if os.name == "nt":
#     asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy


mypath = "/Users/mikolaj/Desktop/emotki"
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

def getRandomEmoteName():
    return random.choice(list(icons.keys()))

def getWeatherInfo(city="Krakow, PL"):
    owm = OWM(token[4])
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
                            with open("/Users/mikolaj/Desktop/emotki/"+icon[0]+".png", "rb") as f:
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
                        with open("/Users/mikolaj/Desktop/emotki/"+e+".png", "rb") as f:
                            files = await client.upload([("emote.png", f, "image/png")])
                        await event.thread.send_text(text=None, files=files)
                    elif(event.message.text=="=status"):
                        await event.thread.send_text("online 🤖")
                    elif(event.message.text=="=help"):
                        msg="Available commands:\n\n=help\n=emotes\n=randomemote\n=status\n=log [msg]\n=links\n=pogoda"
                        await event.thread.send_text(msg)
                    elif(event.message.text.startswith("=log")):
                        msg = event.message.text.split("=log ")[1]
                        with open("logs.txt", "a") as f:
                            f.write("\n"+msg)
                        await event.thread.send_text("logged: "+msg)
                    elif(event.message.text=="=pogoda"):
                        city, w = getWeatherInfo()
                        temp = w.temperature('celsius') 
                        msg = "Pogoda dla "+city+":\n"+str(temp['temp'])+"°C (średnia),\n"+str(temp['feels_like'])+"°C (odczuwalna),\n info: "+ str(w.detailed_status)                     
                        await event.thread.send_text(msg)
                    elif(event.message.text.startswith("=links")):
                        await event.thread.send_text("https://thezapalsky.github.io/links/")
                    elif(event.message.text.startswith("nk ")):
                        await event.thread.send_text("https://www.youtube.com/watch?v=aHtEm9sxzYg")
                    # if(event.message.text==":figiSzlug:"):
                    #     client = fbchat.Client(session=session)
                    #     with open("figiSzlug.png", "rb") as f:
                    #         files = await client.upload([("figiSzlug.png", f, "image/png")])
                    #     await event.thread.send_text(text=None, files=files)
                        #await event.thread.send_text(event.message.text)
            except:
                pass

async def main():
    session = await fbchat.Session.login(email, password)

    client = fbchat.Client(session=session)
    listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

    listen_task = asyncio.create_task(listen(listener, session))

    client.sequence_id_callback = listener.set_sequence_id
    print("fb-bot online")
    # Call the fetch_threads API once to get the latest sequence ID
    await client.fetch_threads(limit=1).__anext__()

    # Let the listener run, otherwise the script will stop
    await listen_task


asyncio.run(main())