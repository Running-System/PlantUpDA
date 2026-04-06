# Plant Up! Performance Analysis Plan

This document outlines the testing strategy to generate empirical data for the **Results and Analysis** chapter of the Plant Up! diploma thesis.

## 1. Throughput & Scalability Test (Python)
**Objective**: Prove the "Thin Edge" architecture handles high-velocity telemetry without dropping messages.

### Stress Test Script (`/tmp/stress_test.py`)
```python
import paho.mqtt.client as mqtt # pip install paho-mqtt
import json
import time
import random

# CONFIGURATION
MQTT_BROKER = "your-broker-address" # e.g. "broker.hivemq.com"
MQTT_TOPIC = "plantup/telemetry"
DEVICE_COUNT = 50   # Simulating 50 individual plants
MESSAGES_PER_DEVICE = 10 

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, 1883, 60)

print(f"Starting Stress Test: {DEVICE_COUNT} devices...")

start_time = time.time()
total_sent = 0

for d in range(DEVICE_COUNT):
    for m in range(MESSAGES_PER_DEVICE):
        payload = {
            "device_id": f"PLANT_SIM_{d:03d}",
            "moisture": round(random.uniform(30.0, 70.0), 2),
            "temp": round(random.uniform(18.0, 26.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2),
            "ts": time.time()
        }
        client.publish(MQTT_TOPIC, json.dumps(payload))
        total_sent += 1
    # Small sleep to avoid network congestion locally
    time.sleep(0.01)

end_time = time.time()
print(f"Test Complete: Sent {total_sent} messages in {end_time - start_time:.2f} seconds.")
client.disconnect()
```

---

## 2. End-to-End Latency Benchmark
**Objective**: Measure the time from physical sensor trigger to database persistence.

| Component | Estimated Latency (ms) | Actual Measured (ms) |
| :--- | :--- | :--- |
| ESP32 Measurement to MQTT Publish | 20ms | [RUN TEST] |
| MQTT Agent to Supabase Insert | 150ms | [RUN TEST] |
| Supabase Real-time to Mobile App | 100ms | [RUN TEST] |
| **Total End-to-End** | **~270ms** | **[FILL IN]** |

---

## 3. Database Optimization (TimescaleDB vs Postgres)
**Objective**: Quantify the performance benefit of hypertable chunking.

Run these in the **Supabase SQL Editor**:

### Test A: Standard Table Scan
```sql
EXPLAIN ANALYZE 
SELECT device_id, AVG(moisture) 
FROM public.standard_telemetry_table
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY device_id;
```

### Test B: TimescaleDB Hypertable Scan
```sql
EXPLAIN ANALYZE 
SELECT device_id, time_bucket('1 hour', time) AS bucket, AVG(moisture)
FROM micro.telemetry_hypertable
WHERE time > NOW() - INTERVAL '7 days'
GROUP BY bucket, device_id;
```

---

## 4. Competitive Comparison (Draft Table for Thesis)
**Objective**: Show **Plant Up!** superiority over traditional architectures.

| Metric | Traditional (Local ESP32 Logic) | Plant Up! (Thin Edge + Cloud AI) |
| :--- | :--- | :--- |
| **Response Flexibility** | Low (New code flash needed) | **High (Cloud update)** |
| **Analysis Power** | Low (ESP32 RAM limited) | **Massive (Postgres + AI)** |
| **Latency** | 10ms (Local) | **~300ms (Cloud)** |
| **Complexity** | High (Multi-protocol sync) | **Medium (Unified API)** |

---

> [!TIP]
> Use these results to justify your **Discussion** chapter. If your system is slower than a local one but provides 10x more data insights, the trade-off is a SUCCESS.
