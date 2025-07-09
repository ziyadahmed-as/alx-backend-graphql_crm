INSTALLED_APPS = [
    ...
    'django_crontab',  # Note: underscore instead of hyphen
    ...
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]