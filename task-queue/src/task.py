from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672/', backend='redis://:password@redis:6379/0')

@app.task
def add(x, y):
    return x + y

result = add.delay(4, 4)
result.ready()
result.get(timeout=1)
result.get(propagate=False)
result.traceback
