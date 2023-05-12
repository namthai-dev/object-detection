from celery import Celery
from redis import Redis
from uuid import uuid4

celery_execute = Celery(broker='amqp://guest:guest@localhost:5672/', backend='redis://:password@localhost:6379/0')
redis = Redis(host="localhost", port="6379", password="password", db="0")

id = str(uuid4())

result = celery_execute.send_task('src.tasks.add', (id, 100, 220))

print("Task id: ", id)

celery_data = result.get()
print("Celery return: ", celery_data)

redis_data = redis.get(id)
print("Redis return: ", redis_data)
