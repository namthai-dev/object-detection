import tensorflow as tf
from .helpers.image import draw_boxes

class Detector(object):
    def __init__(
        self,
        path_to_model,
    ) -> None:
        self.path_to_model = path_to_model
        self.detect_fn = self.load_model()

    def load_model(self):
        module_handle = tf.saved_model.load(self.path_to_model)
        detector = module_handle.signatures["default"]
        return detector
    
    def predict(self, image):
        converted_img  = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
        result = self.detect_fn(converted_img)

        result = {key:value.numpy() for key,value in result.items()}

        image_with_boxes = draw_boxes(
            image.numpy(), result["detection_boxes"],
            result["detection_class_entities"], result["detection_scores"])

        return image_with_boxes
    

class CompletedModel(object):
    def __init__(self) -> None:
        self.model = self._load_model()

    @staticmethod
    def _load_model():
        return Detector(
            path_to_model="./src/ml/models/object-detection"
        )
    
    def detect(self, image):
        image_with_boxes = self.model.predict(image)
        return image_with_boxes