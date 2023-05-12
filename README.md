# object-detection

Ml Models in Production

Serving model using asynchronous Celery tasks and FastAPI

## Architecture

![image](https://github.com/namthai-dev/object-detection/assets/102452878/b83582d8-363e-4f6a-89a5-ce388f43064e)

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
    
## Screenshots

![image](https://github.com/namthai-dev/object-detection/assets/102452878/d7a38555-7261-4dc5-8adf-811743fc7661)

![image](https://github.com/namthai-dev/object-detection/assets/102452878/ffa4f38b-8080-4d0b-bc88-b1fb8490a317)
