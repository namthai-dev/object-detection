import time
from image import draw_boxes, save_image
import tensorflow as tf

def load_model(model_path):
  module_handle = tf.saved_model.load(model_path)
  detector = module_handle.signatures["default"]
  return detector


def run_detector(detector, img, output_path):
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

  save_image(image_with_boxes, output_path)
