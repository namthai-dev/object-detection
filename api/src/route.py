from fastapi import APIRouter, File, Response
import tensorflow as tf
import time
import uuid
from .helpers.image import draw_boxes
import matplotlib.pyplot as plt
from imageio import v3 as iio
import imageio
import io


router = APIRouter(
    prefix="/detect",
    tags=["Object detection"]
)

path = "./src/storage"

@router.post("/")
async def object_detection(img: bytes = File(...)):
    id = uuid.uuid4()
    with open(f"{path}/input/{id}.jpeg",'wb') as image:
        image.write(img)
        image.close()
    image = tf.io.read_file(path + f"/input/{id}.jpeg")
    module_handle = tf.saved_model.load("./src/models/openimages_v4_ssd_mobilenet_v2_1")
    detector = module_handle.signatures["default"]
    image = tf.image.decode_jpeg(image, channels=3)
    converted_img  = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()
    result = {key:value.numpy() for key,value in result.items()}
    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)
    image_with_boxes = draw_boxes(
      image.numpy(), result["detection_boxes"],
      result["detection_class_entities"], result["detection_scores"])
    plt.imsave(f"{path}/output/{id}.jpeg", image_with_boxes)
    return id


@router.get("/image/{id}")
def get_image(id: str):
    im = imageio.imread(path + "/output/" + f"{id}.jpeg") # 'im' could be an in-memory image (numpy array) instead
    with io.BytesIO() as buf:
        iio.imwrite(buf, im, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
    return Response(im_bytes, media_type='image/jpeg')