import time
from datetime import datetime
from ky039 import KY039

sensor = KY039(channel=0)
last_print = time.time()

while True:
    sensor.read_bpm() 
    
    now = time.time()
    if now - last_print >= 1.0:
        bpm, avg = sensor.read_bpm()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Avg: {avg:>6} | BPM: {bpm:>3}")
        last_print = now
    
    time.sleep(0.05)  
