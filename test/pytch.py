import pytchat
import time
import emoji
import json
import urllib
import os
from pytchat import LiveChat
cwd = os.getcwd()
#print(cwd)

# chat = pytchat.create(video_id="https://www.youtube.com/watch?v=-5KAN9_CzSA", interruptable=False)
chat = LiveChat(video_id="https://www.youtube.com/watch?v=-5KAN9_CzSA", interruptable=False)
while chat.is_alive():
    chatdata = chat.get()
    for c in chatdata.sync_items():
        json = json.loads(c.json())
        print(json['author']['name'])
        #f=urllib.request.urlopen(jd2)
        #fil=f.read()
        #f.close()
        #f2=open("img/img.jpg", "wb")
        #f2.write(fil)
        #f2.close()
        #print(chatdata.json())
#         jd = dict(chatdata.json())
#         print(jd)
        #message=emoji.emojize(c.message, use_aliases=True)
#        print(f"{c.datetime} [{c.author.name}] - {message}")
#         url0=f"{c.imageUrl}"
#         r = requests.get(url=url0, params = '')
#         print(r.json())

    time.sleep(5)

try:
    chat.raise_for_status()
except pytchat.ChatdataFinished:
    print("chat data finished")
except Exception as e:
    print(type(e), str(e))
