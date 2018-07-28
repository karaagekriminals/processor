"""MQTT connection to backend module. Used to test """

import paho.mqtt.client as mqtt

import json

# TODO: Modularise. This should be called by the plugin.


def on_connect(client, userdata, flags, rc):
    """Callback for client connects to the broker."""

    print("Connection returned result: ", rc)  # TODO: Delete.

    # Subscribe to the topic.

    client.subscribe("telemetry/98072d27a984/movement")


def on_message(client, userdata, msg):
    """Callback for PUBLISH message received from server."""

    # TODO: Delete.

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
    """Initiate client to connect to the MQTT server."""

    client = mqtt.Client("myclient")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("admin", "secretpassword")

    host_name = "10.77.0.18"  # TODO: Remove hardcoding.
    client.connect_async(host_name, port=1883, keepalive=60, bind_address="")
    client.loop_start()


if __name__ == "__main__":
    initiate_client()

    # Keep client running indefinitely to see output.

    while True:
        pass
