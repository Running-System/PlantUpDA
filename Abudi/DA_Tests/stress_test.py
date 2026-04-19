import paho.mqtt.client as mqtt
import json
import uuid
import time

# Configuration
BROKER = "localhost" 
PORT = 1883
TOPIC = "plantup/sensor"


# Unique ID for this specific test run
TEST_RUN_ID = f"STRESS_{uuid.uuid4().hex[:6]}" 
DEVICE_COUNT = 50   # Increased for 10,000 total msgs
MSGS_PER_DEVICE = 200 # Total: 50 * 200 = 10,000

client = mqtt.Client()

try:
    client.connect(BROKER, PORT)
except Exception as e:
    print(f"Failed to connect to MQTT Broker at {BROKER}: {e}")
    exit(1)

print(f"Starting Stress Test: {TEST_RUN_ID}")
print(f"Targeting: {DEVICE_COUNT} devices, {MSGS_PER_DEVICE} msgs each.")

total_sent = 0
for d in range(DEVICE_COUNT):
    for m in range(MSGS_PER_DEVICE):
        payload = {
            "light": 300.0 + d,
            "temperature": 22.0 + (m * 0.1),
            "humidity": 55.0,
            "soil_moisture": 45.0,
            "electrical_conductivity": 2.3,
            "test_id": TEST_RUN_ID, 
            "sent_at": time.time()       
        }
        client.publish(TOPIC, json.dumps(payload))
        total_sent += 1
    
    time.sleep(0.05) # Mimic network jitter

print(f"\nSuccessfully queued {total_sent} messages.")
print(f"Check your Supabase for Test ID: {TEST_RUN_ID}")
