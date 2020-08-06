from google.cloud import storage
from picamera import PiCamera
from time import sleep
from PIL import Image
from PIL import ImageStat
import math
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/google_cred.json"

def calculate_brightness(im_file):
    im = Image.open(im_file)
    stat = ImageStat.Stat(im)
    r,g,b = stat.mean
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.68*(b**2))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

#Initialize
camera = PiCamera()
bucket_name = "010_refridgenators"
filename = 'initial.jpg'

while True:
    sleep(2)
    camera.capture(filename)
    brightness = calculate_brightness(filename)
    if brightness > 50:
        upload_blob(bucket_name, filename, filename)
        print('uploaded a file')
