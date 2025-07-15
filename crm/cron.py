import datetime
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """Run every 12 hours; restock products with stock < 10."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = Path("/tmp/low_stock_updates_log.txt")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
        mutation {
          updateLowStockProducts {
            message
            products {
              id
              name
              stock
            }
          }
        }
    """)

    try:
        result = client.execute(mutation)
        data = result["updateLowStockProducts"]
        message = data["message"]
        products = data["products"]

        with log_file.open("a") as f:
            f.write(f"\n[{timestamp}] {message}\n")
            for product in products:
                f.write(f"  · {product['name']} → new stock: {product['stock']}\n")

    except Exception as e:
        with log_file.open("a") as f:
            f.write(f"[{timestamp}] ERROR: {str(e)}\n")

def log_crm_heartbeat():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"
    
    log_file = Path("/tmp/crm_heartbeat_log.txt")
    with open(log_file, "a") as f:
        f.write(log_message)

    # Optional GraphQL hello check
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

        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL hello: {hello_value}\n")

    except Exception as e:
        error_message = f"{timestamp} GraphQL check failed: {str(e)}\n"
        with open(log_file, "a") as f:
            f.write(error_message)
