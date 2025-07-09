INSTALLED_APPS = [
    ...
    'django_crontab',  # Note: underscore instead of hyphen
    'django_celery_beat',
    ...
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
     ('0 */12 * * *', 'crm.cron.update_low_stock'), # New job to update low stock products
]

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
