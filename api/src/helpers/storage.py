import os
from os import path


def create_path(path_dir):
    if path.exists(path_dir):
        pass
    else:
        os.mkdir(path_dir)  
