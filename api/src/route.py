from fastapi import APIRouter, File, Response
import uuid
from imageio import v3 as iio
import imageio
import io
import os
from .helpers.model import load_model, run_detector
from .helpers.image import load_img 


router = APIRouter(
    prefix="/detect",
    tags=["Object detection"]
)

storage_path = "./src/storage"

@router.post("/")
async def object_detection(img: bytes = File(...)):
    # Generate id
    id = uuid.uuid4()
    # Path
    input_path = os.path.join(storage_path, "/input", f"{id}.jpeg")
    output_path = os.path.join(storage_path, "/output", f"{id}.jpeg")
    # Save to FS
    with open(input_path,'wb') as image:
        image.write(img)
        image.close()
    # Load model
    detector = load_model("./src/models/openimages_v4_ssd_mobilenet_v2_1")
    # Read image
    image = load_img(input_path)
    # Run model
    run_detector(detector, image, output_path)
    return id


@router.get("/image/{id}")
def get_image(id: str):
    output_path = os.path.join(storage_path, "/output", f"{id}.jpeg")
    im = imageio.imread(output_path)
    with io.BytesIO() as buf:
        iio.imwrite(buf, im, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
    return Response(im_bytes, media_type='image/jpeg')