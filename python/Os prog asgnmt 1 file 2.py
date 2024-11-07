import threading
import time

counter = 50            #Initializing the counter set to 50
l1 = threading.Lock()   # Lock for P1
l2 = threading.Lock()   # Lock for P2

def P1():
    global counter
    # instead of l1.acquire() and l1.release() I used with l1
    Register_1 = counter    #criticallll sectionnnn
    Register_1 += 10
    time.sleep(1)
    with l1:                #to acquire and release lock1
        with l2:
            counter = Register_1

def P2():
    global counter
    # instead of l2.acquire() and l2.release() I used with l2
    with l1:                    #to acquire and release lock2
        Register_2 = counter    #criticallll sectionnn
        Register_2 -= 10
        time.sleep(1)
        counter = Register_2

if __name__ == "__main__":
    #ccreatingg and startingg threadss
    p1_thread = threading.Thread(target=P1)
    p2_thread = threading.Thread(target=P2)

    p1_thread.start()
    p2_thread.start()

    # this is just to wait for threads to finish
    p1_thread.join()
    p2_thread.join()

    #finally, print statement for final value of the variable counter
    print("Counter value after all:", counter)
