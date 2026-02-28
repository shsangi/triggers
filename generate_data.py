import pandas as pd
from datetime import datetime
import pytz
import os

def get_pakistan_time():
    """Get current time in Pakistan timezone"""
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')

def main():
    # File path
    csv_file = 'data_log.csv'
    
    # Timestamps
    current_pakistan_time = get_pakistan_time()
    script_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Get the next serial number
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        try:
            existing_df = pd.read_csv(csv_file)
            next_srno = len(existing_df) + 1
        except:
            # If file is empty or corrupted, start fresh
            next_srno = 1
    else:
        next_srno = 1
    
    # Create new row
    new_row = pd.DataFrame([{
        'srno': next_srno,
        'current_pakistan_timestamp': current_pakistan_time,
        'script_run_timestamp': script_start_time,
        'script_end_timestamp': None,  # Will be filled after any processing
        'tag': 'testing'
    }])
    
    # Simulate some processing time (optional)
    # import time
    # time.sleep(2)
    
    # Update end timestamp
    new_row.loc[0, 'script_end_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Write to CSV
    if os.path.exists(csv_file):
        # Append without header
        new_row.to_csv(csv_file, mode='a', header=False, index=False)
        print(f"✅ Appended row {next_srno} to {csv_file}")
    else:
        # Create new file with header
        new_row.to_csv(csv_file, index=False)
        print(f"✅ Created {csv_file} with first row")
    
    # Display the last few rows for verification
    print("\n📊 Current CSV contents:")
    df = pd.read_csv(csv_file)
    print(df.tail())
    
    # Create a verification file for GitHub Actions to check
    with open('last_run.txt', 'w') as f:
        f.write(f"Last run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total rows: {len(df)}")

if __name__ == "__main__":
    main()
