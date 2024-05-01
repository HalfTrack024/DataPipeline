from opcua import Client, Node
import sys
import time

url = "opc.tcp://127.0.0.1:4840"

try:
    client = Client(url)
    client.connect()
    print("Connected")
except Exception as err:
    print("Error: ", err)
    sys.exit(1)

class subHandler(object):
    def datachange_notification(self, node, value, data):
        url = 'http://your-api-endpoint.com/data'
        payload = {'value': value}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        print(f"POST request sent. Status Code: {response.status_code}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    root = client.get_root_node()

    num_node = client.get_node("ns=2; i=3")

    handler = subHandler()
    sub = client.create_subscription(500, handler)

    handle = sub.subscribe_data_change(num_node)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
