# c:\Users\Abudi\Desktop\PlantUpDA\Abudi\sql_benchmarks\supabase_explain_runner.py
import requests
import re
import csv
import time

# CONFIGURATION
SUPABASE_URL = "https://uxfmopiuedhaoooyhjnw.supabase.co"
ANON_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV4Zm1vcGl1ZWRoYW9vb3loam53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2OTI0OTksImV4cCI6MjA1NzI2ODQ5OX0.H9um-KnTLtJ-1HB0lOPou1ZtIQYJO6AiRW3ECAVYLXU"# <--- PASTE YOUR ANON TOKEN FROM THE .env FILE
ITERATIONS = 100

def get_internal_execution_time(table_type):
    """
    Calls the custom RPC 'get_exact_benchmark_plan' via Supabase API.
    """
    headers = {
        "apikey": ANON_TOKEN,
        "Authorization": f"Bearer {ANON_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{SUPABASE_URL}/rest/v1/rpc/get_exact_benchmark_plan"
    
    try:
        response = requests.post(url, headers=headers, json={"tbl_type": table_type})
        
        if response.status_code != 200:
            print(f"❌ Supabase API Error ({table_type}): {response.status_code}")
            return None
        
        plan_text = response.json()
        
        # Regex to find: "Execution Time: 0.123 ms"
        match = re.search(r"Execution Time: ([\d\.]+) ms", plan_text)
        if match:
            return float(match.group(1))
        
        return None
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def main():
    if ANON_TOKEN == "[YOUR_ANON_TOKEN]":
        print("❌ Error: Please paste your ANON_TOKEN into Line 9 of this script.")
        return

    print(f"🚀 Starting 100-Iteration Benchmark...")
    print(f"Targeting: {SUPABASE_URL}")

    stats = []
    for i in range(1, ITERATIONS + 1):
        t_std = get_internal_execution_time("standard")
        t_hyp = get_internal_execution_time("hypertable")
        
        if t_std is not None and t_hyp is not None:
            stats.append({"run": i, "standard_ms": t_std, "hypertable_ms": t_hyp})
        
        if i % 10 == 0:
            print(f"  Processed {i}/{ITERATIONS}...")

    if not stats:
        print("❌ No data collected. Make sure you ran the SQL to create 'get_exact_benchmark_plan'.")
        return

    # Export to CSV
    filename = 'supabase_explain_results.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["run", "standard_ms", "hypertable_ms"])
        writer.writeheader()
        writer.writerows(stats)

    # Print Summary
    avg_std = sum(s['standard_ms'] for s in stats) / len(stats)
    avg_hyp = sum(s['hypertable_ms'] for s in stats) / len(stats)

    print("\n" + "="*45)
    print("📊 FINAL BENCHMARK RESULTS (AVERAGES)")
    print("="*45)
    print(f"Standard Table:  {avg_std:.4f} ms")
    print(f"Hypertable:      {avg_hyp:.4f} ms")
    print(f"Delta:           {avg_std - avg_hyp:.4f} ms")
    print("="*45)
    print(f"✅ Data saved to: {filename}")

if __name__ == "__main__":
    main()
