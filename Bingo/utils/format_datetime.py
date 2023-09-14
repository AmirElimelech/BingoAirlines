from datetime import datetime

def format_datetime(iso_datetime):
    dt = datetime.fromisoformat(iso_datetime)
    date_str = dt.strftime('%Y-%m-%d')  # gives '2023-09-02'
    time_str = dt.strftime('%H:%M')    # gives '08:24'
    return date_str, time_str
