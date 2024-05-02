from asyncua import Client, Node
import asyncio
import paho.mqtt.publish as publish

class SubscriptionHandler:
    async def datachange_notification(self, node: Node, val, data):
        MQTT_HOST = "localhost"
        node_name = await node.read_display_name()
        node_name = node_name.Text
        MQTT_TOPIC = f"opc/{node_name}"
        MQTT_MESSAGE = val

        publish.single(MQTT_TOPIC, MQTT_MESSAGE, hostname=MQTT_HOST)


        print(f"Data change at node {node}: {val}")

class ADSSubscriptionHandler:
    async def call_back(notification, data):
        print(f"Notification for {notification}: {data}")
