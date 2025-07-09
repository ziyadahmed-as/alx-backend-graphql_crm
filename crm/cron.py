
import datetime
from pathlib import Path

def log_crm_heartbeat():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"
    
    log_file = Path("/tmp/crm_heartbeat_log.txt")
    with open(log_file, "a") as f:
        f.write(log_message)
    
    # Optional GraphQL check
    try:
        # Your GraphQL query implementation here
        pass
    except Exception as e:
        error_message = f"{timestamp} GraphQL check failed: {str(e)}\n"
        with open(log_file, "a") as f:
            f.write(error_message)