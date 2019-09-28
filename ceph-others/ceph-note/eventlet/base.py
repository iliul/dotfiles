import eventlet
import time

def add(a,b):
    # time.sleep(2)   #cost 10s total
    eventlet.sleep(2)   #cost 2s total
    return a+b

pool = eventlet.GreenPool(10)

data = [(1,2),(3,4),(5,6),(7,8),(9,10)]

results = []

for i in data:
    # print i[0],i[1]
    # pass
    results.append(pool.spawn(add,i[0],i[1]))

r = []

start = time.time()
for u in results:
    res = u.wait()
    print res
    r.append(res)

print r
print time.time() - start
