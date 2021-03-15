import multiprocessing
import time

def sd(con, con2,q): #can communicate with main and ud
    while True:
        #reading from server
        recieved = con[1].recv()                       #once something is in the pipe, store it in recieved
        myInt = int(recieved)*int(recieved)            #square it
        
        #writing to ud
        con2[0].send(myInt)

        #reading from ud
        new_out = con2[1].recv()
        
        #writing to server
        q.put(new_out)
    
def ud(con2,q): #can only communicate with sd
    while True:
        #reading
        inp = con2[1].recv()        #once something is in the pipe, store it in recieved
        inp *= 2
        concat = [inp, inp-5]
        
        #writing
        con2[0].send(concat)
    
if __name__ == "__main__":
    
    # creating a pipe
    sd_conn, ud_conn = multiprocessing.Pipe()
    sd_conn2, ud_conn2 = multiprocessing.Pipe()
    
    #establishing connections in pipes
    con = [sd_conn, ud_conn] #renaming for easier use of pipes
    con2 = [sd_conn2, ud_conn2]
    
    q = multiprocessing.Queue()
    
    p1 = multiprocessing.Process(target=sd, args=(con, con2, q))
    p1.start()
    
    p2 = multiprocessing.Process(target=ud, args=(con2,q))
    p2.start()
    
    while 1:
        userInp = input("Please enter a number, or q to quit: ")
        userInp = userInp.upper()
        if (userInp == "Q"):
            break
        con[0].send(userInp)
        time.sleep(0.1)
        while q.empty() is False:
            print(q.get())
        time.sleep(.5)