from threading import Thread
import time

#Setting up the initial values of variables
counter = 10    #counter equals to 10
turn = 0        #turn equals to 0 at the beginning
flag = [False, False]   #setting false values to both processes flag[0] and flag[1]

def P1():   #function for Process 1
    global counter, turn    #access to be able to change the values of counter and turn variables
    flag[0] = True      #Process 1 set to true
    turn = 0            #Process 1's turn

    while flag[1] and turn == 0:    #Peterson's solution appppilcation to Process 1
        pass

    Register_1 = counter        #critical sectionnn
    Register_1 += 2
    time.sleep(1)
    counter = Register_1

    flag[0] = False         #setting flag[0] to false to exit the critical section

def P2():   #function for Process 2
    global counter, turn

    flag[1] = True
    turn = 1

    while flag[0] and turn == 1:    #Peterson's solution appppilcation to Process 2
        pass

    Register_2 = counter            #critical sectionnnn
    Register_2 += 4
    time.sleep(1)
    counter = Register_2

    flag[1] = False                 #setting flag[1] to falseee

#main function to test threads ;)
if __name__ == "__main__":
    p1_thread = Thread(target=P1)       #Creating threads p1 and p2 for
    p2_thread = Thread(target=P2)       #processes P1 and P2 respectively

    p1_thread.start()       #starting threads
    p2_thread.start()

    p1_thread.join()        #to work in accordance
    p2_thread.join()        # with each other

    print("Counter value after both processes:", counter)       #print statement
