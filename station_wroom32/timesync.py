import time
import ntptime


# Global timezone offset in seconds (UTC+2 for Johannesburg)
TIMEZONE_OFFSET = 2 * 3600

# Sync time with NTP and adjust for Johannesburg (UTC+2)
def sync_time_periodically():
    global TIMEZONE_OFFSET 
    while True: 
        ntptime.settime()  # Sync the RTC to UTC
        print("Time synchronized with NTP")
        time.sleep(600)  # Sync every 10 minutes or change to 3600 for every hour

#_thread.start_new_thread(sync_time_periodically, ())

# Custom wrapper for local time with timezone adjustment
def get_adjusted_localtime():
    t = time.localtime(time.time() + TIMEZONE_OFFSET)  # Apply timezone offset
    return t

# Replace get_current_time with RTC time
def get_current_time():
      
    while True: 
        current_time = get_adjusted_localtime()  # Use adjusted time 
        return f"{current_time[0]}-{current_time[1]:02d}-{current_time[2]:02d} {current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}"
