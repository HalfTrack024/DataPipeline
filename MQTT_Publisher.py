import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish




# Define the MQTT server host and port
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
MQTT_MESSAGE = "Hello MQTT"

publish.single(MQTT_TOPIC, MQTT_MESSAGE, hostname=MQTT_HOST)

# Create an MQTT client instance

