#!/usr/bin/env python

# WS client example

import asyncio
import datetime

import websockets

async def hello():
    uri = "ws://localhost:80"
    date = datetime.datetime.now()
    while (True):
        async with websockets.connect(uri) as websocket:
            # name = str(date)#input("What's your name? ")

            # await websocket.send(name)
            # print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")
            await asyncio.sleep(2)

asyncio.get_event_loop().run_until_complete(hello())