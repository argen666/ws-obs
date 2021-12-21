import pytchat
import asyncio
import json
import traceback

from pytchat import ChatDataFinished
from pytchat import LiveChat


async def main():
    print("Chat data started")
    livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=IgE-DV-9z7E", interruptable=False)
    # livechat = LiveChat(video_id="https://www.youtube.com/watch?v=xgirCNccI68", interruptable=False)
    while livechat.is_alive():
        await asyncio.sleep(3)
        chatdata = livechat.get()
        for c in chatdata.sync_items():
            jsondata = json.loads(c.json())
            print(c.json())
            # json.dump(c.json(), json_file, ensure_ascii=False, indent=2)
            # print(jsondata['author']['name'])
    try:
        livechat.raise_for_status()
    except ChatDataFinished:
        print("Chat data finished")
        # loop.close()
    except Exception as e:
        print("Chat data exception")
        # print(traceback.format_exc())
        print(type(e), str(e))
        # loop.close()


# callback function is automatically called periodically.
async def func5(chatdata):
    for c in chatdata.items:
        print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
        await chatdata.tick_async()


if __name__ == '__main__':
    while (True):
        try:
            loop = asyncio.get_event_loop()
            # task = loop.create_task(main())
            loop.run_until_complete(main())
            # loop.run_forever()
            print("123")
            print("123")
            print("123")
            print("123")
        except Exception as ex:
            print("Main exception")
            print(type(ex), str(ex))
            print(traceback.format_exc())
