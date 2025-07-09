import datetime
from celery import shared_task
from pathlib import Path
import requests
import json

@shared_task
def generate_crm_report():
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """
    
    try:
        response = requests.post(
            'http://localhost:8000/graphql',
            json={'query': query},
            headers={'Content-Type': 'application/json'}
        )
        result = response.json()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = Path("/tmp/crm_report_log.txt")
        
        if 'errors' in result:
            log_entry = f"{timestamp} - Error: {result['errors'][0]['message']}\n"
        else:
            data = result['data']
            log_entry = (
                f"{timestamp} - Report: {data['totalCustomers']} customers, "
                f"{data['totalOrders']} orders, {data['totalRevenue']} revenue\n"
            )
        
        with open(log_file, "a") as f:
            f.write(log_entry)
            
        return log_entry
    
    except Exception as e:
        error_msg = f"{timestamp} - Report generation failed: {str(e)}\n"
        with open(log_file, "a") as f:
            f.write(error_msg)
        return error_msg