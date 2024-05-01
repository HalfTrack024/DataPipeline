from asyncua import Client, Node
import asyncio
from pydantic import BaseModel
import SubscriptionHandler as sh

# Global state to store client and subscription
global_client = None
global_subscription = None
handles = {}


# OPC UA client setup
async def opcua_client_setup(endpoint_url):
    global global_client, global_subscription
    if global_client is None:
        global_client = Client(url=endpoint_url)
        await global_client.connect()
        global_subscription = await global_client.create_subscription(500, sh.SubscriptionHandler())


async def opcua_add_subscribers(node_ids):
    global global_client, global_subscription, handles
    # Modify the existing subscription
    if global_subscription and global_client:
        # Remove existing monitored items

        for node_id in node_ids:
            if node_id not in handles:
                node: Node = global_client.get_node(node_id)
                name = await node.read_display_name()
                print(name.Text)
                handles[node_id] = await global_subscription.subscribe_data_change(node)


async def opcua_remove_subscribers(node_ids):
    global global_client, global_subscription, handles
    # Modify the existing subscription
    if global_subscription and global_client:
        # Remove existing monitored items

        for node_id in node_ids:
            if node_id in handles:
                handle = handles[node_id]
                await global_subscription.unsubscribe(handle)
                handles.pop(node_id)



