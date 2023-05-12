from celery import Celery
from redis import Redis
from uuid import uuid4
import time

celery_execute = Celery(broker='amqp://guest:guest@localhost:5672/', backend='redis://:password@localhost:6379/0')
redis = Redis(host="localhost", port="6379", password="password", db="0")

id = str(uuid4())

# Test simple celery
# result = celery_execute.send_task('src.tasks.add', (id, 100, 220))
# print("Task id: ", id)
# celery_data = result.get()
# print("Celery return: ", celery_data)

# Test object detection
object_detection_result = celery_execute.send_task('object_detection_task', ["test"])
while(True):
    celery_data_ob = object_detection_result.get()
    print("Celery return: ", celery_data_ob)
    time.sleep(3)
