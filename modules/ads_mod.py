import ctypes
import pyads
from pyads import Connection, NotificationAttrib
from ctypes import sizeof
from datatypes.TagDefinition import TagDefinition
from SubscriptionSingleton import subscriptions
import paho.mqtt.publish as publish

global_AMS_plc = '192.168.56.101.1.1'
global_port = pyads.PORT_TC3PLC1
handles = {}
tags = {'MAIN.il': pyads.PLCTYPE_INT}
#
plc: Connection = None
#
# plc.open()

def callback(notification, data):
    global plc
    tag = subscriptions[0] #next((subscription for subscription in subscriptions if subscription.name == data), None)
    print(tag.data_type)
    data_type = tag.data_type
    handle, timestamp, value = plc.parse_notification(notification, data_type)
    print(value)
    MQTT_HOST = "test.mosquitto.org"
    MQTT_TOPIC = f"ads/{tag.name}"
    MQTT_MESSAGE = value

    publish.single(MQTT_TOPIC, MQTT_MESSAGE, hostname=MQTT_HOST)


async def add_subscriber(tag_name, datatype):
    global global_AMS_plc, global_port, handles, plc
    subscriptions.append(TagDefinition(tag_name, pyads.PLCTYPE_INT))
    if not plc:
        plc = Connection(global_AMS_plc, global_port)

    if not plc.is_open:
        plc.open()

    attr = NotificationAttrib(sizeof(pyads.PLCTYPE_INT)) #  length=pyads.size_of_structure(datatype)

    handle = plc.add_device_notification(tag_name, attr, callback)
    handles[tag_name] = handle
    #plc.close()
    return handle


async def remove_subscriber(tag_name, datatype):
    global global_AMS_plc, global_port, handles, plc
    if not plc:
        plc = Connection(global_AMS_plc, global_port)
    with plc:
        plc.open()
        handle = handles[tag_name]
        plc.del_device_notification(handle)
        plc.close()
        del handles[tag_name]
        return handle

