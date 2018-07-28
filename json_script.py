# MQTT connection to backend module

#import client library
import paho.mqtt.client as mqtt
import json

# callback for client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: ", rc)

    # subscribe to the topic
    client.subscribe("telemetry/98072d27a984/movement")

# callback for PUBLISH message received from server
def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload)
    gyro_data = json_data['gyro']
    accel_data = json_data['accel']
    mag_data = json_data['mag']
    timestamp = json_data['timestamp']

    print("Gyroscope data:\n", gyro_data)
    print("Accelerometer data\n", accel_data)
    print("Magnetometer data\n", mag_data)
    print("Timestamp\n", timestamp)

def initiate_client():
    client = mqtt.Client("myclient")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("admin", "secretpassword")

    host_name = "10.77.0.18"
    client.connect_async(host_name, port=1883, keepalive=60, bind_address="")
    client.loop_start()

if __name__ == "__main__":
    initiate_client()
    while True:
        pass