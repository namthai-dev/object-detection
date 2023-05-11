from model import run_detector
from image import download_and_resize_image
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

run_detector(detector, downloaded_image_path)