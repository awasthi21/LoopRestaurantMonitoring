
from celery import Celery
from celery.schedules import crontab
import os
from datetime import datetime
from loguru import logger
from RestaurantMonitoring.commons import *
app = Celery('restaurant_polling', broker='redis://localhost:6379/0')
import pytz

@app.task
def poll_restaurant_status_csv_from_server():
    logger.info('Starting poll_restaurant_status_csv_from_server')

    # Get the timestamp
    curr_timestamp = datetime.now(pytz.utc)
    timestamp=curr_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    logger.debug(f'Timestamp: {timestamp}')
    file_name=curr_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
    # Generate the custom migration name
    migration_name = f"populate_restaurant_status_{file_name}.py"
    logger.debug(f'Migration name: {migration_name}')

    # Call the makemigrations command with the custom migration name
    new_migration_file_path=create_custom_migration(migration_name,curr_timestamp)
    logger.debug('makemigrations command executed.')


    logger.info("Call Migration ",migration_name)
    try:
        call_migration_by_name(migration_name)
    except :
        os.remove(new_migration_file_path)
        
        
    logger.info('Migrate command executed.')

# Schedule the task to run every hour
app.conf.beat_schedule = {
    'poll-restaurant-status-csv-now': {
        'task': 'restaurant_polling.poll_restaurant_status_csv_from_server',
        'schedule': crontab(minute=0, hour='*/1'),
        'args': (),
        'kwargs': {},
        'options': {'queue': 'default'},
        'relative': False
    },
}