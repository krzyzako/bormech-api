import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

logger = logging.getLogger(__name__)


@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://krzyzak.duckdns.org/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    yield from C.subscribe([
        ('test/#', QOS_1),
        ('stacja/#', QOS_2),
    ])
    logger.info("Subscribed")
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet 
            pub = str(packet.payload.data.decode('utf-8'))
            print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data.decode('utf-8'))))
            if (pub == 'siema'):
              task = [asyncio.create_task(C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=0x00)),
                      asyncio.create_task(C.publish('a/c', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
                      asyncio.create_task(C.publish('a/d', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),]
              yield from asyncio.wait(task)

        yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())