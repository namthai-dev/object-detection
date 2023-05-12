from redis import Redis
from celery import Celery


redis = Redis(host="redis", port="6379", password="password", db="0")

celery_execute = Celery(broker='amqp://guest:guest@rabbitmq:5672/', backend='redis://:password@redis:6379/0')
