import datetime

def log(message):
    """
    Simple logging function with timestamp.
    """
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
