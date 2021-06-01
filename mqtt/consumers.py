from channels.consumer import SyncConsumer
from datetime import datetime, timedelta
from .models import Mqtt
from homolog.models import Rodzaj
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
channel_layer = get_channel_layer()


class MqttConsumer(SyncConsumer):
    def mqtt_check(self, event):
        time = datetime.now()
        topic = event['text']['topic']
        payload = event['text']['payload']
        print(payload['value'])
        try:
            data = Rodzaj.objects.get(symbol=payload["value"])

            data = {
                'bit': True,
                'reset':False,
                'error':False,
                'poj': data.capacity,
                'homologacja': data.approval,
                'waga': data.weight,
                'srednica': data.dimeter,
            }
           
            print(data)
            print("topic: {0}, payload: {1} time {2}".format(
                topic, payload, time.strftime("%H:%M:%S")))
            
            async_to_sync(channel_layer.send)(
                'mqtt', {'type': 'mqtt.pub', 'text': {'topic': 'stacja/status/', 'payload': data}})
        except:
            data = {
                "bit": False,
                'reset' : False,
                "error": True,
                'poj': 0,
                'homologacja': '',
                'waga': 0.0,
                'srednica': 0,
            }
            print(data)
            async_to_sync(channel_layer.send)(
                'mqtt', {'type': 'mqtt.pub', 'text': {'topic': 'stacja/status/', 'payload': data}})

    def mqtt_save(self, event):
        pass

    def mqtt_sub(self, event):
        time = datetime.now()
        topic = event['text']['topic']
        payload = event['text']['payload']

    def mqtt_pub(self, event):
        # time = datetime.now()
        topic = event['text']['topic']
        payload = event['text']['payload']
        print(payload)
