INSTALLED_APPS = [
    ...
    'django_crontab',  # Note: underscore instead of hyphen
    ...
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
     ('0 */12 * * *', 'crm.cron.update_low_stock'), # New job to update low stock products
]
