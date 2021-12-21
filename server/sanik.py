import asyncio
import json
import os
import re
import signal
import urllib

import pytchat
import socketio
from pytchat import ChatDataFinished
from pytchat.util import extract_video_id
from sanic import Sanic
from sanic import response
from sanic.response import html

sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins=[])
app = Sanic(name='ws-obs')
sio.attach(app)


@sio.event
async def ws_connect(sid, message):
    streamUrl = message['stream_url']
    await collect_chat_data(None, urllib.parse.unquote(streamUrl))


@sio.event
async def ws_disconnect(sid, message):
    await sio.disconnect(sid)
    stopWorkerThread()


# @app.websocket('/')
# async def feed(request, ws):
#     # await collect_chat_data(ws, "https://www.youtube.com/watch?v=IgE-DV-9z7E")
#     await collect_chat_data(ws, urllib.parse.unquote(request.args.get("url")))


@app.route('/chat')
async def handle_request(request):
    streamUrl = urllib.parse.quote_plus(request.args.get("url"))
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ws-obs.html')
    with open(file) as f:
        content = f.read()
        content = re.sub("{stream_url}", streamUrl, content)
        return html(content)


@app.route('/html2')
async def handle_request(request):
    streamUrl = request.args.get("url")
    return response.html(f"""<html><head><script>
         var exampleSocket = new WebSocket("ws://" + location.host + '/?url={streamUrl}');
         exampleSocket.onmessage = function (event) {{
         console.log(event.data) }};</script></head><body><h1>Hello socket!</h1><p>hello111</p></body></html>""")


@app.listener("after_server_start")
async def listener_3(app, loop):
    print("LISTENER 3")
    # task = loop.create_task(main())


@app.listener("before_server_stop")
async def before_server_stop(app, loop):
    stopWorkerThread()


async def collect_chat_data(ws, streamUrl):
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
                await sio.emit('message', jsondata)

                # await ws.send(c.json())
                await asyncio.sleep(5)
        try:
            livechat.raise_for_status()
        except ChatDataFinished:
            print("Chat data finished")
            livechat.terminate()
            await sio.emit('alert_reload', {'error': 'ChatDataFinished'})
        except Exception as e:
            print("Chat data exception")
            livechat.terminate()
            await sio.emit('alert_reload', {'error': str(e)})
            # print(traceback.format_exc())
            print(type(e), str(e))
    else:
        print("Stream URL is empty or not valid. Please check the Stream URL in the script settings")


def isYoutubeVideoIdValid(streamUrl):
    try:
        vid = extract_video_id(streamUrl)
        # r = requests.get(f'https://img.youtube.com/vi/{id}/mqdefault.jpg')
        # return r.status_code == 200
        return True
    except Exception as ex:
        print(type(ex), str(ex))
        return False


def stopWorkerThread():
    global isWorkerStarted
    isWorkerStarted = False
    # print("Stop worker...")


def startWorkerThread():
    global isWorkerStarted
    isWorkerStarted = True
    # print("Stop worker...")


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    exit(signum)


def start():
    # loop = asyncio.get_event_loop()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js')
    path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
    print(path)
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    app.static('/js', path)
    app.static('/img', path2)
    app.run(host="0.0.0.0", port=80, debug=True)

    futures = []
    # futures.append(server)
    print("789")
    # while (True):
    #     try:
    #         loop = asyncio.get_event_loop()
    #         # task = loop.create_task(main())
    #         # futures.append(main())
    #         # loop.run_until_complete(main())
    #         loop.run_until_complete(server)
    #         # loop.run_forever()
    #         print("123")
    #         print("123")
    #         print("123")
    #     except Exception as ex:
    #         print("Main exception")
    #         print(type(ex), str(ex))
    #         print(traceback.format_exc())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    start()
