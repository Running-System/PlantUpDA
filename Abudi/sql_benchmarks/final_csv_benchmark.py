# c:\Users\Abudi\Desktop\PlantUpDA\Abudi\sql_benchmarks\final_csv_benchmark.py
import requests
import re
import csv

# CONFIG
SUPABASE_URL = "https://uxfmopiuedhaoooyhjnw.supabase.co"
ANON_TOKEN = "[YOUR_ANON_TOKEN]" # <--- PASTE FROM .env
ITERATIONS = 100

def run():
    if ANON_TOKEN == "[YOUR_ANON_TOKEN]":
        print("❌ Error: Set your ANON_TOKEN.")
        return

    headers = {
        "apikey": ANON_TOKEN,
        "Authorization": f"Bearer {ANON_TOKEN}",
        "Content-Type": "application/json"
    }
    
    rows = []
    print(f"🚀 Collecting {ITERATIONS} data points...")

    try:
        for i in range(1, ITERATIONS + 1):
            # 1. Standard
            r1 = requests.post(f"{SUPABASE_URL}/rest/v1/rpc/get_exact_benchmark_plan", headers=headers, json={"tbl_type": "standard"})
            t_std = float(re.search(r"Execution Time: ([\d\.]+) ms", r1.json()).group(1))

            # 2. Hypertable
            r2 = requests.post(f"{SUPABASE_URL}/rest/v1/rpc/get_exact_benchmark_plan", headers=headers, json={"tbl_type": "hypertable"})
            t_hyp = float(re.search(r"Execution Time: ([\d\.]+) ms", r2.json()).group(1))

            rows.append({"run": i, "standard_ms": t_std, "hypertable_ms": t_hyp})
            if i % 10 == 0: print(f"  Progress: {i}%")

        with open('final_benchmark_results.csv', 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=["run", "standard_ms", "hypertable_ms"])
            w.writeheader()
            w.writerows(rows)

        print("-" * 30)
        print(f"✅ DONE. Data saved to final_benchmark_results.csv")
        print(f"Avg Standard: {sum(r['standard_ms'] for r in rows)/ITERATIONS:.3f}ms")
        print(f"Avg Hyper:    {sum(r['hypertable_ms'] for r in rows)/ITERATIONS:.3f}ms")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
