import os
import time
import random
import json
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/temperature")
SENSOR_ID = os.getenv("SENSOR_ID", "sensor-1")
INTERVAL = float(os.getenv("PUBLISH_INTERVAL", "1.0"))

client = mqtt.Client(client_id=f"temp-{SENSOR_ID}")


def connect():
    while True:
        try:
            print(f"Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT}...")
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            print("Connected to MQTT broker.")
            return
        except Exception as e:
            print(f"MQTT connection failed: {e}. Retry in 3 seconds...")
            time.sleep(3)


def main():
    connect()
    client.loop_start()

    try:
        while True:
            temperature = round(random.uniform(60, 100), 2)
            payload = {
                "sensor_id": SENSOR_ID,
                "temperature": temperature,
            }
            msg = json.dumps(payload)

            print(f"Publish: topic={MQTT_TOPIC}, payload={msg}")
            client.publish(MQTT_TOPIC, msg)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Stopping sensor...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
