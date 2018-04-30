import time
import io
import os
import shutil
import h5py
import threading
import picamera
import tensorflow as tf
import numpy as np
from PIL import Image
from keras.models import load_model


class LazyModel:
    def __init__(self,server=None,model_name='model5',num_of_batch=25):
        self.camera=picamera.PiCamera()
        self.camera.resolution = (320,240)
        self.camera.rotation=180
        self.camera.framerate=40
        self.num_of_batch=num_of_batch
        self.img_list=[]
        self.img_path='./images'
        self.model_name=model_name
        self.s=server
        self.stop=False
        self.graph = None

        
    
    def predict(self):
        with self.graph.as_default():
            print('Starting model')
            i=1
            while(not self.stop):
                if(os.path.isdir(self.img_path) and len(os.listdir(self.img_path))>200):
                    t_colored_images=[]
                    t_labels=[]
                    files=sorted(os.listdir(self.img_path))
                    for im in range(len(files)-self.num_of_batch,len(files)):
                        colored_image = Image.open(self.img_path+'/'+files[im]).convert('RGB')
                        colored_image = colored_image.resize((100,132),Image.ANTIALIAS)
                        colored_image = np.array(colored_image,dtype=np.float32)
                        colored_image = colored_image/255
                        t_colored_images.append(np.array(colored_image))
                    with self.graph.as_default():
                        conclusion=self.model.predict(np.array(t_colored_images))
                    other_things=0
                    drumming_fingers=0
                    pulling_hand_in=0
                    pulling_hand_away=0
                    for a in conclusion:
                        other_things+=a[0]*100
                        drumming_fingers=a[1]*100
                        pulling_hand_in+=a[2]*100
                        pulling_hand_away+=a[3]*100
                    other_things/=self.num_of_batch
                    drumming_fingers/=self.num_of_batch
                    pulling_hand_in/=self.num_of_batch
                    pulling_hand_away/=self.num_of_batch
                    print('===========================================')
                    print('prediction:',i)
                    print(conclusion)
                    print('other things:',other_things,'%')
                    print('drumming fingers:',drumming_fingers,'%')
                    print('pulling hand in:',pulling_hand_in,'%')
                    print('pushing hand away:',pulling_hand_away,'%')
                    print('===========================================')
                    i+=1
    
    def outputs(self):
        if(not os.path.isdir('images')):
            os.makedirs('images')
        stream = io.BytesIO()
        print('Starting to capture video')
        while (not self.stop):
            # This returns the stream for the camera to capture to
            yield stream
            # Once the capture is complete, the loop continues here
            # (read up on generator functions in Python to understand
            # the yield statement). Here you could do some processing
            # on the image...
            #stream.seek(0)
            if(len(os.listdir(self.img_path))==500):
                files=sorted(os.listdir(self.img_path))
                os.remove(self.img_path+'/'+files[0])
            img = Image.open(stream)
            img.save('./images/image-'+str(time.time())+'.jpg')
            # Finally, reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
    
    def start_camera(self,pic_resolution=[132,100]):
        self.model = load_model(self.model_name+'.h5py')
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()
        threading.Thread(self.predict()).start()
        self.camera.capture_sequence(self.outputs(), 'jpeg', use_video_port=True,resize=pic_resolution)
        if(os.path.isdir('images')):
            shutil.rmtree('images')
            
    def stop_all(self):
        self.stop=True
        
m=LazyModel()
m.start_camera()