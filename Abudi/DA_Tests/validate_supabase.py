from supabase import create_client
import sys
import datetime

# Configuration (Managed by Antigravity)
SUPABASE_URL = "https://uxfmopiuedhaoooyhjnw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV4Zm1vcGl1ZWRoYW9vb3loam53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2OTI0OTksImV4cCI6MjA1NzI2ODQ5OX0.H9um-KnTLtJ-1HB0lOPou1ZtIQYJO6AiRW3ECAVYLXU"

def validate(test_id):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print(f"Analyzing End-to-End Metrics for ID: {test_id}...")
    
    try:
        # We query the 'Controllers' table in the 'microcontroller_schema'
        # We select 'sent_at' (device timestamp) and 'created_at' (Supabase insertion timestamp)
        response = supabase.schema("microcontroller_schema").table("Controllers") \
            .select("id, sent_at, created_at", count="exact") \
            .eq("test_id", test_id) \
            .execute()
        
        records = response.data
        count = response.count
        expected = 10000 # Matches updated stress_test.py config
        
        if count == 0:
            print(f"\n[!] No records found for ID {test_id}.")
            print("Ensure the C# Middleware is running and the 'test_id' column exists in Supabase.")
            return

        latencies = []
        arrival_times = []
        
        for r in records:
            if r.get('sent_at') and r.get('created_at'):
                try:
                    # Device send time (Unix timestamp)
                    send_time = float(r['sent_at'])
                    
                    # DB arrival time (ISO string to Unix timestamp)
                    # Supports various ISO formats, including Z suffix
                    db_time_raw = r['created_at'].replace('Z', '+00:00')
                    db_time = datetime.datetime.fromisoformat(db_time_raw).timestamp()
                    
                    latency = db_time - send_time
                    if latency > 0: # Filter out clock sync issues if any
                        latencies.append(latency)
                        
                    arrival_times.append(db_time)
                except (ValueError, TypeError):
                    continue

        # Throughput Calculation
        if len(arrival_times) > 1:
            duration = max(arrival_times) - min(arrival_times)
            mps = count / duration if duration > 0 else count
        else:
            duration = 0
            mps = 0

        avg_latency_ms = (sum(latencies) / len(latencies)) * 1000 if latencies else 0

        print(f"\n" + "="*50)
        print(f" THIN EDGE E2E VALIDATION: {test_id}")
        print(f"="*50)
        print(f"Packets Received: {count} / {expected}")
        print(f"Success Rate:     {(count / expected) * 100:.2f}%")
        print(f"Avg. E2E Latency: {avg_latency_ms:.2f} ms")
        print(f"Peak Throughput:  {mps:.2f} messages/sec")
        print(f"Total Transit:    {duration:.2f} seconds")
        print(f"="*50)
        
        if count >= expected:
            print("\nVERDICT: SYSTEM STABLE - Zero Packet Loss confirmed.")
        elif count > expected * 0.95:
            print("\nVERDICT: ACCEPTABLE - Low packet loss under stress.")
        else:
            print("\nVERDICT: CRITICAL - High packet loss or bottleneck detected.")

    except Exception as e:
        print(f"\n[ERROR] Validation failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate(sys.argv[1])
    else:
        tid = input("Enter the TEST_ID from your stress test: ")
        validate(tid)
