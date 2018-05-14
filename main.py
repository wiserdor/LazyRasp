from RPIClient import RPIClient

s=RPIClient()
s.connect

from LazyModel import LazyModel

m=LazyModel(server=s,model_name='model_lstm',num_of_batch=15)
m.start()
##
##
##while 1:
##    if(s.connected):
##        break
##time.sleep(3)
##print('play')
##for i in reversed(range(0,6)):
##    print(i)
##    time.sleep(1)
##s.send('play')
##print('next')
##
##for i in reversed(range(0,6)):
##    print(i)
##    time.sleep(1)
##s.send('next')
##print('back')
##
##for i in reversed(range(0,5)):
##    print(i)
##    time.sleep(1)
##s.send('back')
##print('next')
##
##for i in reversed(range(0,6)):
##    print(i)
##    time.sleep(1)
##s.send('next')
##print('next')
##
##for i in reversed(range(0,5)):
##    print(i)
##    time.sleep(1)
##s.send('next')
##print('play')
##
##for i in reversed(range(0,5)):
##    print(i)
##    time.sleep(1)
##s.send('play')
##
