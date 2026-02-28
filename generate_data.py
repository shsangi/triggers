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
    
    # ALWAYS add a new row
    if os.path.exists(csv_file):
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
        'current_pakistan_timestamp': pakistan_now.strftime('%Y-%m-%d %H:%M:%S'),
        'script_run_timestamp': now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'script_end_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'tag': 'testing'
    }])
    
    # Append to CSV
    if os.path.exists(csv_file):
        new_row.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        new_row.to_csv(csv_file, index=False)
    
    print(f"✅ Added row {next_srno} at {pakistan_now.strftime('%H:%M:%S')}")
    
    # Create verification file
    with open('last_run.txt', 'w') as f:
        f.write(f"Last run: {datetime.now()}\n")
        f.write(f"Rows in CSV: {next_srno}\n")

if __name__ == "__main__":
    main()
