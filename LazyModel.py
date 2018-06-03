import time
import io
import os
import shutil
import threading
from PIL import Image


class LazyModel:
    def __init__(self,camera,gui,server=None,lann=None):
        print('starting LazyModel.py')
        self.camera=camera
        self.gui=gui
        self.camera.resolution = (800,608)
        self.camera.rotation=180
        self.camera.framerate=10
        self.img_path='./images'
        self.s=server
        self.lann=lann
        self.stop=False
        self.lock = threading.Lock()

    def remove_file(self,file_path):
        os.remove(file_path)
        
    def check_if_dir_exists(self):
        #lock.acquire() # thread blocks at this line until it can obtain lock
        if(not os.path.isdir(self.img_path)):
            os.makedirs('images')
       # lock.release()
       

    def predict(self):
        print('LazyModel:prediction started')
        while(not self.stop):
            self.lock.acquire() # thread blocks at this line until it can obtain lock
            if(len(os.listdir(self.img_path))>40):
                files=sorted(os.listdir(self.img_path))
                self.lock.release()
                starttime=time.time()
                conclusion=self.lann.predictme('./images/'+files[-1])
                end=time.time()
                print('===========================================')
                print(end-starttime)
                print('===========================================')
            else:
                self.lock.release()
        print('LazyModel:predict stopped')

    
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
    
            if(len(os.listdir(self.img_path))== 60):
                files=sorted(os.listdir(self.img_path))
                self.remove_file(self.img_path+'/'+files[0])
            img = Image.open(stream)
            img.save('./images/image-'+str(time.time())+'.jpg')
            self.lock.release()

            # Finally, reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
        print('LazyModel:outputs stopped')
    
    def start_camera(self,pic_resolution=[800,608]):
        try:
            self.camera.capture_sequence(self.outputs(), 'jpeg', use_video_port=True,resize=pic_resolution)
        except:
            print('LazyModel:camera stopped')
            
    def connection_manager(self):
        while 1:
            if self.stop==False:
                if not self.s.isConnected:
                    print('LazyModel: Not connected, stopping...')
                    self.stop_all()
                elif self.gui.isTraining:
                    print('LazyModel: training new model, stopping...')
                    self.stop_all()
            elif self.s.isConnected and not self.gui.isTraining:
                self.resume
            time.sleep(1)
    
    def start(self):
        self.check_if_dir_exists()
        self.t3=threading.Thread(target=self.connection_manager).start()
        self.t1=threading.Thread(target=self.start_camera).start()
        self.t2=threading.Thread(target=self.predict).start()
        
    def resume(self):
        print('LazyModel: Resuming...')
        self.stop=False
        self.check_if_dir_exists()
        self.t1.join()
        self.t2.join()
        self.t1.start()
        self.t2.start()
        
    def stop_all(self):
        self.stop=True
        if(os.path.isdir('images')):
            shutil.rmtree('images')
