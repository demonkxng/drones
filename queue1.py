import time
import multiprocessing as mp
import sys

x = []

def inp(xq):
    for i in range(5):
        
        xq.put(6*i)
        time.sleep(1)

def printer(xq):
    for i in range(5):
        time.sleep(1)
        print("entered")
        sys.stdout.write("entered")
        # print(x[:],y[:],z[:])
        


if __name__ == '__main__':
    xq = mp.Queue()
    # x=mp.Array('f', 0)
    # y=mp.Array('f', 0)
    # z=mp.Array('f', 0)
    
    
    mp1 = mp.Process(target=inp, args=(xq,))
    mp2 = mp.Process(target=printer, args=(xq,))
    
    mp1.start()
    mp2.start()
    
    mp1.join()
    mp2.join()
    print(x)
    print("done")