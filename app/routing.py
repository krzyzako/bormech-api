from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from mqtt.consumers import MqttConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter(
        {
            "mqtt": MqttConsumer
        }
    )
})