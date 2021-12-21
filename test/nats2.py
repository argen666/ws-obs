import asyncio
import nats
import json

from nats.js.api import ReplayPolicy, ConsumerConfig, DeliverPolicy


async def main():
    nc = await nats.connect()
    print(nc)
    js = nc.jetstream()
    sub = await js.subscribe(stream="youtube-stream", subject="comments", durable="printer",
                             config=ConsumerConfig(replay_policy=ReplayPolicy.instant,
                                                   deliver_policy=DeliverPolicy.all))
    while True:
        try:
            msg = await sub.next_msg()
            jsondata = json.loads(msg.data)
            print(jsondata['author']['name'] + ": " + jsondata['message'])
            await asyncio.sleep(3)
            await msg.ack()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    asyncio.run(main())
