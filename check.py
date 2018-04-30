import picamera
import time

camera=picamera.PiCamera()
camera.resolution = (320,240)
camera.rotation=180
camera.framerate=40

camera.start_preview()
time.sleep(30)
camera.stop_preview()