# CRM Report Generation Setup

## Prerequisites
- Redis server installed and running
- Python 3.8+ with pip

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Start Redis server (if not running):
   ```bash
   redis-server
   ```

## Running the Services
1. Start Celery worker:
   ```bash
   celery -A crm worker -l info
   ```

2. Start Celery Beat (scheduler):
   ```bash
   celery -A crm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

## Verification
1. Check the report log:
   ```bash
   cat /tmp/crm_report_log.txt
   ```

2. Monitor tasks in real-time:
   ```bash
   celery -A crm flower
   ```
   (Then visit http://localhost:5555)

## Schedule Configuration
Reports generate every Monday at 6:00 AM UTC. To modify:
- Edit `CELERY_BEAT_SCHEDULE` in `crm/settings.py`