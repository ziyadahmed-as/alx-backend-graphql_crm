
import datetime
from pathlib import Path

import datetime
from pathlib import Path
import requests
import json

def update_low_stock():
    # GraphQL mutation query
    mutation = """
    mutation {
        updateLowStockProducts {
            products {
                id
                name
                stock
            }
            message
        }
    }
    """
    
    # Execute the mutation (using requests as an example)
    try:
        response = requests.post(
            'http://localhost:8000/graphql',  # Update with your GraphQL endpoint
            json={'query': mutation},
            headers={'Content-Type': 'application/json'}
        )
        result = response.json()
        
        # Log the results
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        log_file = Path("/tmp/low_stock_updates_log.txt")
        
        with open(log_file, "a") as f:
            f.write(f"\n[{timestamp}] Stock Update Results:\n")
            
            if 'errors' in result:
                f.write(f"Error: {result['errors'][0]['message']}\n")
            else:
                data = result['data']['updateLowStockProducts']
                f.write(f"Message: {data['message']}\n")
                for product in data['products']:
                    f.write(f"Updated: {product['name']} (New stock: {product['stock']})\n")
    
    except Exception as e:
        # Log any errors
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] Failed to update stock: {str(e)}\n")

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