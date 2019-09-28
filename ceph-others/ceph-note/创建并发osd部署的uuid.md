```
#for i in `seq 1 10`;do python generate_var.py 5 > hosts_dir/192.168.1.$i ;done
```

```
#!/usr/bin/python
import uuid
import sys
from jinja2 import Template
from string import ascii_lowercase
import itertools
template = Template(
'---\ndisks_var: "{{disks_var}}"\ndevices_data_uuids_var: "{{devices_data_uuids_var}}"\ndevices_journal_uuids_var: "{{devices_journal_uuids_var}}"')

def iter_all_strings():
    size = 1
    while True:
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)
        size +=1
gen = iter_all_strings()
def label_gen():
    for s in gen:
        return s

disks=[]
devices_data_uuids =[]
devices_journal_uuids =[]
label_gen()
for i in range(1,int(sys.argv[1])+1):
    disks.append('/dev/sd'+label_gen())
    devices_data_uuids.append(str(uuid.uuid1()))
    devices_journal_uuids.append(str(uuid.uuid1()))

print template.render(disks_var=disks,devices_data_uuids_var=devices_data_uuids,devices_journal_uuids_var=devices_journal_uuids)
```
