import pickle, multiprocessing #-
from socket   import *         #-
from time     import sleep     #-
from random   import *         #-
from constRPC import *         #-
#-
from client   import *         #-
from server   import *         #-
from dbclient import *         #-
#-
# Execução local (parte a): hosts fixos em 'localhost'.
# As constantes HOSTS/HOSTC1/HOSTC2 de constRPC.py guardam IPs da nuvem (parte b).
LOCAL = 'localhost'

def client1():
  c1   = Client(PORTC1)                # create client
  dbC1 = DBClient(LOCAL,PORTS)         # create reference
  dbC1.create()                        # create new list
  dbC1.appendData('Client 1')          # append some data
  c2 = multiprocessing.Process(target=client2).start() # create 2nd client #-
  sleep(2)                             # make sure the other client is running #-
  c1.sendTo(LOCAL,PORTC2,dbC1)         # send to other client

def client2():
  c2   = Client(PORTC2)                # create a new client
  data = c2.recvAny()                  # block until data is sent
  dbC2 = pickle.loads(data)            # receive reference
  dbC2.appendData('Client 2')          # append data to same list
  print(dbC2.getValue()) #-
  c2.sendTo(LOCAL,PORTS,[STOP]) #-

def server(): #-
  server = Server(PORTS) #-
  c1 = multiprocessing.Process(target=client1).start() # create 1st client #-
  server.run() #-
#-
if __name__ == "__main__": #-
#-
  s = multiprocessing.Process(target=server) #-
  s.start() #- 
  s.join() #-
