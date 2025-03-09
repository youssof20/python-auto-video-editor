import datetime

def log(message, to_file=True):
    """
    Simple logging function with timestamp.
    Logs to both console and file.
    """
    log_message = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_message)
    
    if to_file:
        # Save log to file
        with open('process_log.txt', 'a') as f:
            f.write(log_message + '\n')
