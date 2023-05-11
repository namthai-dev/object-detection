# object-detection

Ml Models in Production

Serving model using asynchronous Celery tasks and FastAPI

## Setup

Create environment

    conda create -n object-detection python=3.9 -y

Activate

    conda activate object-detection

Install dependency

    cd api/
    poetry install

Install tensorflow

    https://www.tensorflow.org/install/pip
    
## Run

Run API service

    cd api
    ./run.py

## Models

    https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1

    https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1