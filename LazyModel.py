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
from keras.backend import tensorflow_backend as K


class LazyModel:
    def __init__(self,server=None,model_name='model5',num_of_batch=25):
        self.camera=picamera.PiCamera()
        self.camera.resolution = (320,240)
        self.camera.rotation=180
        self.camera.framerate=15
        self.num_of_batch=num_of_batch
        self.img_list=[]
        self.img_path='./images'
        self.model_name=model_name
        self.s=server
        self.stop=False
        self.graph = None
        self.lock = threading.Lock()

    def remove_file(self,file_path):
        os.remove(file_path)
        
    def check_if_dir_exists(self):
        #lock.acquire() # thread blocks at this line until it can obtain lock
        if(not os.path.isdir(self.img_path)):
            os.makedirs('images')
       # lock.release()

    
    def predict(self):
        print('prediction started')
        with self.graph.as_default():  
            while(not self.stop):
                self.lock.acquire() # thread blocks at this line until it can obtain lock
                if(len(os.listdir(self.img_path))>40):
                    t_colored_images=[]
                    t_labels=[]
                    files=sorted(os.listdir(self.img_path))
                    for im in range(len(files)-self.num_of_batch,len(files)):
                        colored_image = Image.open(self.img_path+'/'+files[im]).convert('RGB')
                        colored_image = colored_image.resize((100,132),Image.ANTIALIAS)
                        colored_image = np.array(colored_image,dtype=np.float32)
                        colored_image = colored_image/255
                        t_colored_images.append(np.array(colored_image))
                    self.lock.release()
                    starttime=time.time()
                    with self.graph.as_default():
                        conclusion=self.model.predict(np.array(t_colored_images))
                    end=time.time()
                    
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
                    print(conclusion)
                    print('other things:',other_things,'%')
                    print('drumming fingers:',drumming_fingers,'%')
                    print('pulling hand in:',pulling_hand_in,'%')
                    print('pushing hand away:',pulling_hand_away,'%')
                    print(end-starttime)
                    print('===========================================')
                else:
                    self.lock.release()

    
    def outputs(self):
        
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
            self.lock.acquire() # thread blocks at this line until it can obtain lock
    
            if(len(os.listdir(self.img_path))==150):
                files=sorted(os.listdir(self.img_path))
                self.remove_file(self.img_path+'/'+files[0])
            img = Image.open(stream)
            img.save('./images/image-'+str(time.time())+'.jpg')
            self.lock.release()

            # Finally, reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
            
    
    def start_camera(self,pic_resolution=[132,100]):
        self.camera.capture_sequence(self.outputs(), 'jpeg', use_video_port=True,resize=pic_resolution)

    
    def start(self):
        with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=4)) as sess:
            K.set_session(sess)
        self.model = load_model(self.model_name+'.h5py')
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()
        self.check_if_dir_exists()
        t1=threading.Thread(target=self.start_camera).start()
        t2=threading.Thread(target=self.predict).start()
            
    def stop_all(self):
        self.stop=True
        if(os.path.isdir('images')):
            shutil.rmtree('images')
        
m=LazyModel()
m.start()