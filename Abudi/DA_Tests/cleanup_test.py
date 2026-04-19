from supabase import create_client
import sys

# Configuration (Managed by Antigravity)
SUPABASE_URL = "https://uxfmopiuedhaoooyhjnw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV4Zm1vcGl1ZWRoYW9vb3loam53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2OTI0OTksImV4cCI6MjA1NzI2ODQ5OX0.H9um-KnTLtJ-1HB0lOPou1ZtIQYJO6AiRW3ECAVYLXU"

def cleanup(test_id):
    if not test_id.startswith("STRESS_"):
        confirm = input(f"Warning: {test_id} does not look like a stress test ID. Are you sure you want to delete these records? (y/n): ")
        if confirm.lower() != 'y':
            print("Cleanup cancelled.")
            return

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print(f"Purging records for Test ID: {test_id}...")
    
    try:
        # Targeting the microcontroller_schema.Controllers table
        response = supabase.schema("microcontroller_schema").table("Controllers") \
            .delete() \
            .eq("test_id", test_id) \
            .execute()
        
        # response.data contains the deleted rows
        deleted_count = len(response.data) if response.data else 0
        
        print(f"\n" + "-"*40)
        print(f" CLEANUP SUCCESSFUL")
        print(f"-"*40)
        print(f"Records Deleted: {deleted_count}")
        print(f"-"*40)

    except Exception as e:
        print(f"\n[ERROR] Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cleanup(sys.argv[1])
    else:
        tid = input("Enter the TEST_ID to purge from database: ")
        if tid:
            cleanup(tid)
        else:
            print("No Test ID provided.")
