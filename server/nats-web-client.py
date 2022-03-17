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

# sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins=[])
app = Sanic(name='ws-obs')
# sio.attach(app)


@app.route('/chat')
async def handle_request(request):
    streamUrl = urllib.parse.quote_plus(request.args.get("url"))
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ws-obs-nats.html')
    with open(file) as f:
        content = f.read()
        content = re.sub("{nats_host}", streamUrl, content)
        return html(content)

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


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    start()
