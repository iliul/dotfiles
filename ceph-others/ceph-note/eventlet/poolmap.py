import eventlet
import time
import hashlib

def add(data):
    # time.sleep(2)
    eventlet.sleep(data[1])
    return data[0] + data[1],hashlib.sha256(str(data[0]+data[1])).hexdigest()

pool = eventlet.GreenPool(10)
data = [(2,10),(3,8),(1,6),(4,4),(5,2)]
results = []
start = time.time()
res = pool.imap(add,data)
for i in res:
    print time.time() - start ,i,i[0],i[1]
    results.append(i[0])
print time.time()-start
print results
