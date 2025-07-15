INSTALLED_APPS = [
    # other apps...
    'django_crontab',
    'django_celery_beat',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

# Celery broker (Redis)
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Celery Beat schedule for weekly report on Monday at 6:00 AM
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}