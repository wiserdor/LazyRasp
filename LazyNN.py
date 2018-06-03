
# coding: utf-8

# In[1]:


import cv2
import keras
from keras.backend import tensorflow_backend as K
import tensorflow as tf
from keras import Model
from keras.models import Sequential,load_model
import urllib.request
import os
import numpy as np
import time
#import picamera
from picamera.array import PiRGBArray

# In[30]:

class LazyNN:
    
    def __init__(self,camera,model_name='lazy_mod'):
        self.xs=None
        self.ys=None
        self.num_Of_Classes=5
        self.dense_size=8
        self.learning_rate=0.0001
        self.model_name=model_name
        self.img_in_class=15
        self.img_num=0
        with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=4)) as sess:
            K.set_session(sess)
        self.graph = tf.get_default_graph()
        self.oldx=None
        self.camera=camera
        if os.path.isfile('./Models/lazy_mod.h5py'):
            self.model = load_model('./Models/'+self.model_name+'.h5py')
            self.model._make_predict_function()
        else:
            self.model=None
        self.mobile=self.load_mobilenet()


    
        
    
    def capture(self,label):
        img_counter = 0
        rawCapture = PiRGBArray(self.camera,size=tuple([800,600]))

        for f in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = f.array
            k = cv2.waitKey(1)
            if k%256 == 27:
                print("Escape hit, closing...")
                break  
            img_name = "opencv_frame_{}.png".format(img_counter)
            #cv2.imwrite(img_name, frame)
            img =cv2.resize(frame,dsize=(224,224), interpolation = cv2.INTER_CUBIC)
            np_image_data = np.asarray(img)
            np_image_data=cv2.normalize(np_image_data.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
            np_final = np.expand_dims(np_image_data,axis=0)
            #np_final=np.asarray(np_final,dtype='float')
            #m=np.asarray(self.mobile.predict(np_final),dtype='float')
            if self.oldx is None:
                self.oldx=np_final
                self.ys=label
            else:
                self.oldx=np.concatenate((self.oldx,np_final),axis=0)
                self.ys=np.vstack((self.ys,label))
                print("{} written!".format(img_name))
                img_counter += 1
            rawCapture.truncate(0)
            if img_counter==self.img_in_class:
                break
        self.img_num=self.img_num+img_counter
        rawCapture.close()
        
    def open_cam(self):
        self.camera=picamera.PiCamera()
        self.camera.resolution = (800,600)
        self.camera.rotation=180
        self.camera.framerate=5
        
        
    def addexample(self,label):
        """0-left 1-right 2-up 3-down 4-ok 5-back 6-noise """
        one_pos = int(label)
        y = np.zeros(self.num_Of_Classes)
        y[one_pos] = 1
        self.capture(y)
        print(self.img_num)

        
         
    def load_mobilenet(self):
        mobilenet=keras.applications.mobilenet.MobileNet(input_shape=None, alpha=1.0, depth_multiplier=1, dropout=1e-3, include_top=True, weights='imagenet', input_tensor=None, pooling=None, classes=1000)
        return Model(inputs=mobilenet.inputs,outputs=mobilenet.get_layer('conv_pw_13_relu').output)

    def train(self):
        with self.graph.as_default():
            for x in self.oldx:
                image_expand= np.expand_dims(x,axis=0)
                m=np.asarray(self.mobile.predict(image_expand),dtype='float')
                if self.xs is None:
                    self.xs=m
                else:
                    self.xs=np.concatenate((self.xs,m),axis=0)

                
            
            model = Sequential([
            keras.layers.Flatten(input_shape=[7, 7, 1024]),
             keras.layers.Dense(units=self.dense_size,activation='relu',kernel_initializer=keras.initializers.VarianceScaling(),use_bias=True),
            keras.layers.Dense(units=self.num_Of_Classes,activation='softmax',kernel_initializer=keras.initializers.VarianceScaling(),use_bias=False),
            ])
            adam=keras.optimizers.Adam(lr=self.learning_rate)
            model.compile(loss=keras.losses.categorical_crossentropy, optimizer=adam)
            batch=self.img_num 
            model.fit(x=self.xs, y=self.ys,batch_size=batch, epochs= 600)
            self.model=model
            model.save('./Models/lazy_mod.h5py')
    
    def predictme(self,img_path):
        with self.graph.as_default():

            img_counter = 0
            
            frame=cv2.imread(img_path)
            img =cv2.resize(frame,dsize=(224,224), interpolation = cv2.INTER_CUBIC)
            np_image_data = np.asarray(img)
            np_image_data=cv2.normalize(np_image_data.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
            np_final = np.expand_dims(np_image_data,axis=0)
            m=np.asarray(self.mobile.predict(np_final),dtype='float')
            output= self.model.predict_classes(m)
            print(output)
            if output==0:
                print("left")
            elif output==1:
                print("right")
            elif output==2:
                print("up")
            elif output==3:
                print("down")
            elif output==4:
                print("ok")
            elif output==5:
                print("noise")
            return output
        
        

        


# In[31]:


##def main():
##    w=LazyNN()
##    usr=input("do you want to start adding examples? y/n")
##    while(usr=='y'):
##        w.addexample()
##        usr=input("do you want to keep adding?")
##    usr=input("train me?\n y/n")
##    if (usr=='y'):
##        w.train()
##    usr=input("predict? y/n")
##    if (usr=='y'):
##        w.predictme()            
##
##
##if __name__== "__main__":
##  main()
    

