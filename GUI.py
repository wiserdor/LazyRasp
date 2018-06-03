import tkinter as tk
import tkinter.font
import os
import time
import threading


class GUI(threading.Thread):
    def __init__(self,lazynn=None):
        threading.Thread.__init__(self)
        self.lazynn=lazynn
        self.is_training=False
    
    def execute(self):
        threading.Thread(target=self.train_model).start()
        
    def isTraining(self):
        return self.is_training
    
    def run(self):
        self.win=tk.Tk()
        self.win.title("Lazy")
        self.win.geometry('320x240')
        top_frame=tk.Frame(self.win,bg='CadetBlue1',width=320,height=50)
        btm_frame=tk.Frame(self.win,bg='white',width=320,height=190)
        top_frame.grid(row=0,sticky='NEWS')
        btm_frame.grid(row=1,sticky='EWNS')
        self.label=tk.Label(btm_frame,text='^_^',background='white',font=tkinter.font.Font(family='Helvetica',size=32,weight='bold'))
        self.label.place(relx=0.5,rely=0.5,anchor='center')
        self.train_button=tk.Button(top_frame,text="Train",font=tkinter.font.Font(family='Helvetica',size=36,weight='bold'),foreground='white',command=self.execute,height=1,width=5,background='gray')
        self.train_button.place(relx=0.5,rely=0.5,anchor='center')
        tk.mainloop()
    
    def train_model(self):
        self.is_training=True
        #self.laztnn.open_cam()
        cl_list=['left','right','up','down','ok']
        print("training...")
        self.label.config(text="Lets Start...")
        time.sleep(2)
        self.label['text']='Get ready...'
        time.sleep(2)
        for i in range(len(cl_list)):
            self.label['text']='Do '+cl_list[i]
            time.sleep(1)
            self.label['text']='In'
            time.sleep(1)
            self.label['text']='3'
            time.sleep(1)
            self.label['text']='2'
            time.sleep(1)
            self.label['text']='1'
            time.sleep(1)
            self.label['text']='Capturing '+cl_list[i]+'...'
            self.lazynn.addexample(i)
        self.label['text']='We are training...'
        self.lazynn.train()
        self.label['text']='We all set (='
        time.sleep(1)
        self.is_training=False
        
if __name__=='__main__':
    g=GUI()
        
    