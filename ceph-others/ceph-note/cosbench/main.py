from mako.template import Template
def buildxmlforget(workloadname,accesskey,secretkey,endpoint,workers,totalOps,cprefix,oprefix):
    result = Template(filename='get.txt').render(workloadname=workloadname,
                                                 accesskey=accesskey,
                                                 secretkey=secretkey,
                                                 endpoint=endpoint,
                                                 workstagename=workers,
                                                 workname=workloadname,
                                                 workers=workers,
                                                 totalOps=totalOps,
                                                 cprefix=cprefix,
                                                 oprefix=oprefix)
    with open(workloadname+'.xml', 'w') as f:
        f.write(result)

def buildxmlforput(workloadname,accesskey,secretkey,endpoint,workers,totalOps,cprefix,oprefix,sizes):
    result = Template(filename='put.txt').render(workloadname=workloadname,
                                                 accesskey=accesskey,
                                                 secretkey=secretkey,
                                                 endpoint=endpoint,
                                                 workstagename=workers,
                                                 workname=workloadname,
                                                 workers=workers,
                                                 totalOps=totalOps,
                                                 cprefix=cprefix,
                                                 oprefix=oprefix,
                                                 sizes=sizes)
    with open(workloadname+'.xml', 'w') as f:
        f.write(result)

def buildxmlfordel(workloadname, accesskey, secretkey, endpoint, workers, totalOps, cprefix, oprefix):
    result = Template(filename='delete.txt').render(workloadname=workloadname,
                                                 accesskey=accesskey,
                                                 secretkey=secretkey,
                                                 endpoint=endpoint,
                                                 workstagename=workers,
                                                 workname=workloadname,
                                                 workers=workers,
                                                 totalOps=totalOps,
                                                 cprefix=cprefix,
                                                 oprefix=oprefix)
    with open(workloadname + '.xml', 'w') as f:
        f.write(result)

def buildgroup(putname,getname,delname,ak,sk,host,workers,total,cp,op,size):
    buildxmlforput(putname,ak,sk,host,workers,total,cp,op,size)
    buildxmlforget(getname,ak,sk,host,workers,total,cp,op)
    buildxmlfordel(delname,ak,sk,host,workers,total,cp,op)


buildgroup('PUT-64K-100W-OPS100000',
           'GET-64K-100W-OPS100000',
           'DEL-64K-100W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           100,
           100000,
           'cosbench-yuliyang',
           '100wks_64K',
           '(64)KB')

buildgroup('PUT-512K-100W-OPS100000',
           'GET-512K-100W-OPS100000',
           'DEL-512K-100W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           100,
           100000,
           'cosbench-yuliyang',
           '100wks_512K',
           '(512)KB')

buildgroup('PUT-4M-100W-OPS100000',
           'GET-4M-100W-OPS100000',
           'DEL-4M-100W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           100,
           100000,
           'cosbench-yuliyang',
           '100wks_4M',
           '(4)MB')

# =================================================================


buildgroup('PUT-64K-500W-OPS100000',
           'GET-64K-500W-OPS100000',
           'DEL-64K-500W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           500,
           100000,
           'cosbench-yuliyang',
           '500wks_64K',
           '(64)KB')

buildgroup('PUT-512K-500W-OPS100000',
           'GET-512K-500W-OPS100000',
           'DEL-512K-500W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           500,
           100000,
           'cosbench-yuliyang',
           '500wks_512K',
           '(512)KB')

buildgroup('PUT-4M-500W-OPS100000',
           'GET-4M-500W-OPS100000',
           'DEL-4M-500W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           500,
           100000,
           'cosbench-yuliyang',
           '500wks_4M',
           '(4)MB')

#======================================================
buildgroup('PUT-64K-1000W-OPS100000',
           'GET-64K-1000W-OPS100000',
           'DEL-64K-1000W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           1000,
           100000,
           'cosbench-yuliyang',
           '1000wks_64K',
           '(64)KB')


buildgroup('PUT-512K-1000W-OPS100000',
           'GET-512K-1000W-OPS100000',
           'DEL-512K-1000W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           1000,
           100000,
           'cosbench-yuliyang',
           '1000wks_512K',
           '(512)KB')

buildgroup('PUT-4M-1000W-OPS100000',
           'GET-4M-1000W-OPS100000',
           'DEL-4M-1000W-OPS100000',
           'cosbench-yuliyang',
           'cosbench-yuliyang',
           'http://10.128.3.68/',
           1000,
           100000,
           'cosbench-yuliyang',
           '1000wks_4M',
           '(4)MB')



