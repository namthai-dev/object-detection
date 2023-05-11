import time
from image import download_and_resize_image, load_img, draw_boxes, save_image
import tensorflow as tf

tf.config.list_physical_devices('GPU')

image_url = "https://upload.wikimedia.org/wikipedia/commons/6/60/Naxos_Taverna.jpg"  #@param
downloaded_image_path = download_and_resize_image(image_url, 1280, 856, True)

# Hub load
# import tensorflow_hub as hub
# module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
# detector = hub.load(module_handle).signatures['default']

# Local load
module_handle = tf.saved_model.load("./models/openimages_v4_ssd_mobilenet_v2_1")
detector = module_handle.signatures["default"]

img = load_img(downloaded_image_path)

converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
start_time = time.time()
result = detector(converted_img)
end_time = time.time()

result = {key:value.numpy() for key,value in result.items()}

print("Found %d objects." % len(result["detection_scores"]))
print("Inference time: ", end_time-start_time)

image_with_boxes = draw_boxes(
    img.numpy(), result["detection_boxes"],
    result["detection_class_entities"], result["detection_scores"])

save_image(image_with_boxes, "./storage/output", "img_test.jpg")
