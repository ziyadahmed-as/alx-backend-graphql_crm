#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import pytz

# Define timestamp
timestamp = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

# GraphQL transport setup
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Date range: last 7 days
seven_days_ago = (datetime.now(pytz.utc) - timedelta(days=7)).date().isoformat()

# Define GraphQL query
query = gql("""
    query GetRecentOrders($fromDate: Date!) {
        orders(orderDate_Gte: $fromDate) {
            id
            customer {
                email
            }
        }
    }
""")

# Execute query with variable
params = {"fromDate": seven_days_ago}
response = client.execute(query, variable_values=params)

# Log file path
log_file = "/tmp/order_reminders_log.txt"

# Write results to log
with open(log_file, "a") as f:
    for order in response.get("orders", []):
        order_id = order["id"]
        email = order["customer"]["email"]
        f.write(f"[{timestamp}] Reminder: Order ID {order_id}, Customer Email: {email}\n")

# Console confirmation
print("Order reminders processed!")
