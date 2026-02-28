import pandas as pd
from datetime import datetime
import pytz
import os

def get_pakistan_time():
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.now(pakistan_tz)

def main():
    csv_file = 'data_log.csv'
    
    # Get current time
    now = datetime.now()
    pakistan_now = get_pakistan_time()
    
    # Read existing CSV or create new
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        try:
            df = pd.read_csv(csv_file)
            next_srno = len(df) + 1
            print(f"📊 Existing rows: {len(df)}")
        except Exception as e:
            print(f"⚠️ Error reading CSV: {e}")
            next_srno = 1
    else:
        next_srno = 1
        print("📁 Creating new CSV")
    
    # Create new row
    new_row = pd.DataFrame([{
        'srno': next_srno,
        'current_pakistan_timestamp': pakistan_now.strftime('%Y-%m-%d %H:%M:%S'),
        'script_run_timestamp': now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'script_end_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'tag': 'testing'
    }])
    
    # Append to CSV
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        new_row.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        new_row.to_csv(csv_file, index=False)
    
    print(f"✅ Added row {next_srno} at {pakistan_now.strftime('%H:%M:%S')}")
    
    # Create verification file
    with open('last_run.txt', 'w') as f:
        f.write(f"Last run: {datetime.now()}\n")
        f.write(f"Row added: {next_srno}\n")
        f.write(f"Pakistan time: {pakistan_now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Double-check CSV was written
    if os.path.exists(csv_file):
        final_df = pd.read_csv(csv_file)
        print(f"📊 Total rows now: {len(final_df)}")
    else:
        print("❌ CSV not found after write!")

if __name__ == "__main__":
    main()
