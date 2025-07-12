import datetime
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests
import json

def update_low_stock():
    # (your existing code remains unchanged)
    ...

def log_crm_heartbeat():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"
    
    log_file = Path("/tmp/crm_heartbeat_log.txt")
    with open(log_file, "a") as f:
        f.write(log_message)

    # ✅ Optional GraphQL hello check using gql
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
            hello
        }
        """)

        response = client.execute(query)
        hello_value = response.get("hello", "No response")

        # Log hello field result
        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL hello: {hello_value}\n")

    except Exception as e:
        error_message = f"{timestamp} GraphQL check failed: {str(e)}\n"
        with open(log_file, "a") as f:
            f.write(error_message)
