import pandas as pd
from datetime import datetime
import pytz
import os

def get_pakistan_time():
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')

def main():
    csv_file = 'data_log.csv'
    
    # Get current timestamps
    current_pakistan_time = get_pakistan_time()
    script_run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Determine next serial number
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        try:
            df = pd.read_csv(csv_file)
            next_srno = len(df) + 1
        except:
            next_srno = 1
    else:
        next_srno = 1
    
    # Create new row
    new_row = pd.DataFrame([{
        'srno': next_srno,
        'current_pakistan_timestamp': current_pakistan_time,
        'script_run_timestamp': script_run_timestamp,
        'script_end_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'tag': 'testing'
    }])
    
    # Write to CSV
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        new_row.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        new_row.to_csv(csv_file, index=False)
    
    print(f"✅ Added row {next_srno} at {current_pakistan_time}")
    
    # Verify
    df = pd.read_csv(csv_file)
    print(f"📊 Total rows: {len(df)}")

if __name__ == "__main__":
    main()
