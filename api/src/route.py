from fastapi import APIRouter, File, Response
import uuid
from imageio import v3 as iio
import imageio
import io
import os
from os import path
from .mq_main import celery_execute, redis

router = APIRouter(
    prefix="/detect",
    tags=["Object detection"]
)

storage_path = "./storage"

@router.post("/")
async def object_detection(img: bytes = File(...)):
    # Generate id
    id = str(uuid.uuid4()) + ".jpg"
    # Create path
    create_path(storage_path + "/input")
    # Path
    input_path = storage_path + f"/input/{id}"
    # Save to FS
    with open(input_path,'wb') as image:
        image.write(img)
        image.close()
    # Send task to celery
    celery_execute.send_task('object_detection_task', [id])
    return id


@router.get("/image/{id}")
def get_image(id: str):
    create_path(storage_path + "/output")
    output_path = storage_path + f"/output/{id}"
    im = imageio.imread(output_path)
    with io.BytesIO() as buf:
        iio.imwrite(buf, im, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
    return Response(im_bytes, media_type='image/jpeg')


@router.get("/status/{id}")
def get_status(id: str):
    result = redis.get(id)
    return result



def create_path(path_dir):
    if path.exists(path_dir):
        pass
    else:
        os.mkdir(path_dir)  