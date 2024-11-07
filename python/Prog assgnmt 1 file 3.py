from threading import Thread
import threading
import time

#global variables to be useddd
buffer = [-1 for i in range(100)]    #holds up to 50 pairs(100 each shoe) of shoes, initially -1(empty)
index_produced = 0                  #index of produced pairs
index_consumed = 0                  #index of consumed pairs

# Initializing Semaphores: X, Y and Z
X = threading.Semaphore()
Y = threading.Semaphore(100)
Z = threading.Semaphore(0)

#producer functionn for shoes production
def Producer():
    #getting access to be able to change the values of global vairables
    global buffer, index_produced, index_consumed
    global X, Y, Z          #and semaphores

    #we need 50 pairs to be produced, so the it ranges between 1 and 51
    for produced_pair in range(1, 51):
        Y.acquire()
        X.acquire()

        buffer[index_produced] = produced_pair     #placeing the pairs into buffer
        index_produced = index_produced + 1        #move to next index,
        buffer[index_produced] = produced_pair     #2 for each pair
        index_produced = index_produced + 1
        print(f"Producer executed: {produced_pair} pairs has been produced")

        X.release()
        Z.release()

        time.sleep(1)

#consumer functionn for shoes consuming ;)
def Consumer():
    #getting access to be able to change the values of global vairables
    global buffer, index_produced, index_consumed
    global X, Y, Z          #and semaphores


    for i in range(50):
      Z.acquire()
      X.acquire()

      shoes = buffer[index_consumed]           #fetching the pair from the buffer
      index_consumed = index_consumed + 2      #moving to the next index
                                                #2 for pair of shoes
      print(f"Consumed {shoes} pairs")
      print("-------------------------------")

      X.release()
      Y.release()

      time.sleep(2)

#Main()
if __name__ == "__main__":
    # Creating Threadssss
    p1_thread = Thread(target=Producer)
    p2_thread = Thread(target=Consumer)

    # just starting them
    p1_thread.start()
    p2_thread.start()

    # just to wait threads to finish theri work
    p1_thread.join()
    p2_thread.join()
