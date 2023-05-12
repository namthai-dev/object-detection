from celery import Celery, Task
from redis import Redis
import logging
from .ml.model import CompletedModel
from .ml.helpers.image import load_img, save_image
from .helpers.storage import create_path

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672/', backend='redis://:password@redis:6379/0')
redis = Redis(host="redis", port="6379", password="password", db="0")

@app.task
def add(task_id, x, y):
    redis.set(task_id, x + y)
    return x + y


class PredictTask(Task):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            self.model = CompletedModel()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)
    

@app.task(
        bind=True,
        base=PredictTask,
        name="object_detection_task"
)
def object_detection_task(self, task_id: str):
    try:
        create_path("./storage/input")
        create_path("./storage/output")
        img = load_img(f"./storage/input/{task_id}")
        image_with_boxes = self.model.detect(img)
        save_image(image_with_boxes, f"./storage/output/{task_id}")
        redis.set(task_id, "ok")
        return "ok"
    except:
        redis.set(task_id, "error")
        return "error"