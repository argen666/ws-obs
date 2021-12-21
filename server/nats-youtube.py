import asyncio
import json
import os
import re
import signal
import sys
import urllib
import traceback

import pytchat

from pytchat import ChatDataFinished
from pytchat.util import extract_video_id
import nats
from nats.js.api import RetentionPolicy, StorageType
from nats.errors import TimeoutError


async def collect_chat_data(nts, streamUrl):
    global isWorkerStarted
    print(str(streamUrl))
    if streamUrl and isYoutubeVideoIdValid(streamUrl):
        print("Chat data started: " + str(streamUrl))
        livechat = pytchat.create(video_id=streamUrl, interruptable=False)
        isWorkerStarted = True
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=-5KAN9_CzSA", interruptable=False)
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=IgE-DV-9z7E", interruptable=False)
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=ThbXM1-Wfyw", interruptable=False)
        while livechat.is_alive():
            await asyncio.sleep(3)
            if not isWorkerStarted:
                print('Received stop flag, terminating')
                livechat.terminate()
                return
            chatdata = livechat.get()
            for c in chatdata.sync_items():
                jsondata = json.loads(c.json())
                # print(c.json())
                print(jsondata['author']['name'] + ": " + jsondata['message'])
                # await ws.send(jsondata['author']['name'] + ": " + jsondata['message'])
                # await sio.emit('message', jsondata)
                ack = await nts.publish("comments", c.json().encode())
                print(ack)
                # await ws.send(c.json())
                await asyncio.sleep(5)
        try:
            livechat.raise_for_status()
        except ChatDataFinished:
            print("Chat data finished")
            livechat.terminate()
            # await sio.emit('alert_reload', {'error': 'ChatDataFinished'})
        except Exception as e:
            print("Chat data exception")
            livechat.terminate()
            # await sio.emit('alert_reload', {'error': str(e)})
            # print(traceback.format_exc())
            print(type(e), str(e))
    else:
        print("Stream URL is empty or not valid. Please check the Stream URL in the script settings")


def stopWorkerThread():
    global isWorkerStarted
    isWorkerStarted = False
    # print("Stop worker...")


def startWorkerThread():
    global isWorkerStarted
    isWorkerStarted = True
    # print("Stop worker...")


def isYoutubeVideoIdValid(streamUrl):
    try:
        vid = extract_video_id(streamUrl)
        # r = requests.get(f'https://img.youtube.com/vi/{id}/mqdefault.jpg')
        # return r.status_code == 200
        return True
    except Exception as ex:
        print(type(ex), str(ex))
        return False


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    exit(signum)


async def connectNats(natsHost):
    nc = await nats.connect()
    js = nc.jetstream()
    from nats.js.errors import NotFoundError
    try:
        # await js.delete_stream(name="youtube-stream"); exit(1)
        await js.stream_info(name="youtube-stream")
    except NotFoundError as ex:
        print("youtube-stream not found, creating...")
        await js.add_stream(name="youtube-stream", subjects=["comments"], retention=RetentionPolicy.limits,
                        storage=StorageType.memory)
                            # , max_msgs=10000, max_age=3)

    # print(await js.stream_info(name="youtube-stream"))
    return js


if __name__ == '__main__':
    nats_host = sys.argv[1]
    stream_url = sys.argv[2]
    signal.signal(signal.SIGINT, handler)
    # nats = connectNats(nats_host)
    while (True):
        try:
            loop = asyncio.get_event_loop()
            nts = loop.run_until_complete(connectNats(nats_host))
            loop.run_until_complete(collect_chat_data(nts, stream_url))
        except Exception as ex:
            print("Main exception")
            print(type(ex), str(ex))
            print(traceback.format_exc())
