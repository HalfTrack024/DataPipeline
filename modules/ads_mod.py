import pyads

global_AMS_plc = '192.168.56.101.1.1'
global_port = pyads.PORT_TC3PLC1
handles = {}
#
# plc = pyads.Connection(global_AMS_plc, global_port)
#
# plc.open()

def callback(adr, notification, user):
    print(f"Notification for {user}: {notification}")

with pyads.Connection(global_AMS_plc, global_port) as plc:
    plc.open()

    try:
        while True:
            il = plc.read_by_name('Main.il', pyads.PLCTYPE_INT)
            print(il)
    except Exception as err:
        print("wee got problem: ", err)
    finally:
        plc.close()


def add_subscriber(tag_name, datatype):
    global global_AMS_plc, global_port, handles
    with pyads.Connection(global_AMS_plc, global_port) as plc:
        plc.open()
        attr = pyads.NotificationAttrib(length=pyads.size_of_structure(datatype))
        handle = plc.add_device_notification(tag_name, attr, callback)
        handles[tag_name] = handle
        plc.close()
    return handle
