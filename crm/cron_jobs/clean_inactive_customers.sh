#!/bin/bash

# Get current script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to Django project root
cd "$SCRIPT_DIR/../../" || {
  echo "Failed to change directory to project root"
  exit 1
}

# Define timestamp
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

# Run Django shell command to delete inactive customers and log results
deleted_count=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff_date)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Append result to log file
echo "[$timestamp] Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
