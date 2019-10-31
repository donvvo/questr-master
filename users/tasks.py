

from celery.utils.log import get_task_logger
from questr.celery import app 
 
from users.contrib import user_handler

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@app.task
def activate_shipper(courier_id):
    """Activates Shipper, this should only be used after a shipper doesn't ack a request"""
    courier = user_handler.getQuestrDetails(int(courier_id))
    user_handler.updateCourierAvailability(courier, True)
    logger.warn("Courier availability set to True")
