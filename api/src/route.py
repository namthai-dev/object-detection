from fastapi import APIRouter, File, Response
import uuid
from imageio import v3 as iio
import imageio
import io
from .helpers.model import load_model, run_detector
from .helpers.image import load_img 
from .helpers.storage import create_path

router = APIRouter(
    prefix="/detect",
    tags=["Object detection"]
)

storage_path = "./storage"

@router.post("/")
async def object_detection(img: bytes = File(...)):
    # Generate id
    id = uuid.uuid4()
    # Create path
    create_path(storage_path + "/input")
    create_path(storage_path + "/output")
    # Path
    input_path = storage_path + f"/input/{id}"
    output_path = storage_path + f"/output/{id}"
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
    create_path(storage_path + "/output")
    output_path = storage_path + f"/output/{id}"
    im = imageio.imread(output_path)
    with io.BytesIO() as buf:
        iio.imwrite(buf, im, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
    return Response(im_bytes, media_type='image/jpeg')