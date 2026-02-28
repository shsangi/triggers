import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

def get_pakistan_time():
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.now(pakistan_tz)

def main():
    csv_file = 'data_log.csv'
    current_time = get_pakistan_time()
    
    # Read existing data or create new
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        df = pd.read_csv(csv_file)
        # Convert to datetime for comparison
        df['current_pakistan_timestamp'] = pd.to_datetime(df['current_pakistan_timestamp'])
        last_time = df['current_pakistan_timestamp'].max()
        next_srno = len(df) + 1
    else:
        # Create with first record
        df = pd.DataFrame()
        last_time = current_time - timedelta(minutes=1)  # Start from previous minute
        next_srno = 1
    
    # Calculate minutes gap
    minutes_gap = int((current_time - last_time).total_seconds() / 60)
    
    # Always ensure we have records for every minute
    records_added = 0
    for i in range(1, minutes_gap + 1):
        record_time = last_time + timedelta(minutes=i)
        
        # Only add if not in future
        if record_time <= current_time:
            new_row = pd.DataFrame([{
                'srno': next_srno,
                'current_pakistan_timestamp': record_time.strftime('%Y-%m-%d %H:%M:%S'),
                'script_run_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'script_end_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'tag': 'testing'
            }])
            
            # Append to CSV
            if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
                new_row.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                new_row.to_csv(csv_file, index=False)
            
            records_added += 1
            next_srno += 1
    
    print(f"✅ Added {records_added} records (filled {minutes_gap} minute gap)")

if __name__ == "__main__":
    main()
