import time

n = 5
w = 30

while(n<=10000):
    start = time.time()
    for x in range(n):
        w = w*2
    n+=100
    end = time.time()
    print(end-start)