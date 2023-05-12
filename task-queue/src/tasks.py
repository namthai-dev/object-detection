from celery import Celery
from redis import Redis

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672/', backend='redis://:password@redis:6379/0')
redis = Redis(host="redis", port="6379", password="password", db="0")

@app.task
def add(task_id, x, y):
    redis.set(task_id, x + y)
    return x + y
