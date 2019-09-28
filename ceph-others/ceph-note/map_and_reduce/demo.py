import os, multiprocessing as mp
import hashlib,time
filename = '/root/DATA/4096MB'
# process file function
def processfile(fn, start=0, stop=0):
    with open(fn, 'r') as fh:
        fh.seek(start)
        data = fh.read(stop - start)
        return hashlib.sha256(data).hexdigest()


def data_sha256(data):
    shalist = []
    off = 0
    datalen = len(data)
    while off < datalen:
        chunk_start = off
        chunk_end = chunk_start + 32768
        if chunk_end > datalen:
            chunk_end = datalen
        chunk = data[chunk_start:chunk_end]
        shalist.append(hashlib.sha256(chunk).hexdigest())
        off += 32768
    return shalist


if __name__ == "__main__":
    filesize = os.path.getsize(filename)
    split_size = 1*1024*1024
    # determine if it needs to be split
    if filesize > split_size:
        pool = mp.Pool(4)
        cursor = 0
        results = []
        start = time.time()
        with open(filename, 'r') as fh:
             # for every chunk in the file...
             for chunk in xrange(filesize // split_size):
                 # determine where the chunk ends, is it the last one?
                 if cursor + split_size > filesize:
                     end = filesize
                 else:
                     end = cursor + split_size
                 # seek to end of chunk and read next line to ensure you
                 # pass entire lines to the processfile function
                 fh.seek(end)
                 # fh.read()
                 # get current file location
                 end = fh.tell()
                 # add chunk to process pool, save reference to get results
                 proc = pool.apply_async(processfile, args=[filename, cursor, end])
                 results.append(proc)
                 # setup next chunk
                 cursor = end

        # close and wait for pool to finish
        pool.close()
        pool.join()
        print time.time() -start,"seconds cost"
        # iterate through results
        for proc in results:
            processfile_result = proc.get()
            print processfile_result


    else:
        print "-------------"
    print "xxxxxxxxxx"

#4GB   
# 15.7944829464 seconds cost

# 2a8eaf399c5e57688a6a199c9a71d4bf7441190148ae85234acac1e1d00bbcf9
# dd49b7a90eb64685b9b8068eb87d53a17b9d8b1859c6e7fdca952e38eac8105b
# 08354a582c960ad3980791125b5f892572791361a32c234f43970d0d9c0ec8da
# 9fc1802f183fdc79f3b8812fb96cbee5a48b830dfe806ea8bd2e27f4ad0d8816
# 64094146df3eff898fafb352365cef76642e2f3cde0a39e8d8ac1d69dbb250c7
# 74d35eb926d33c9f0abe9ec33431038465fc9a644c8a76ad811a453de5d19422
# 13000535ffeb1d1b6085239f9557512de20790f190faf026ce4205587d333aa0

#29.22s
# 2a8eaf399c5e57688a6a199c9a71d4bf7441190148ae85234acac1e1d00bbcf9
# dd49b7a90eb64685b9b8068eb87d53a17b9d8b1859c6e7fdca952e38eac8105b
# 08354a582c960ad3980791125b5f892572791361a32c234f43970d0d9c0ec8da
# 9fc1802f183fdc79f3b8812fb96cbee5a48b830dfe806ea8bd2e27f4ad0d8816
# 64094146df3eff898fafb352365cef76642e2f3cde0a39e8d8ac1d69dbb250c7
# 74d35eb926d33c9f0abe9ec33431038465fc9a644c8a76ad811a453de5d19422
# 13000535ffeb1d1b6085239f9557512de20790f190faf026ce4205587d333aa0
