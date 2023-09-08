from datetime import datetime

def log(*values: object):
    now = datetime.now()
    log_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(log_time, values)



