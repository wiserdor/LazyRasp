import os
import picamera
camera=picamera.PiCamera()
from GUI import GUI
from LazyNN import LazyNN
lnn=LazyNN(camera)

g=GUI(lnn).start()
while(not os.path.isfile('./Models/lazy_mod.h5py')):
    time.sleep(2)
    
from RPIClient import RPIClient

s=RPIClient()
s.connect()

from LazyModel import LazyModel

m=LazyModel(camera=camera,server=s,gui=g,lann=lnn)
m.start()
