远端A机器生成，所有其他机器读取
```
---
- name: create monitor initial keyring
  copy: content="genarate by hosts " dest=/tmp/hello.txt
  run_once: true
  delegate_to:  "{{ groups['test'][0] }}"

- name: fetch contents of mon_secret file
  slurp: path=/tmp/hello.txt
  run_once: true
  delegate_to: "{{ groups['test'][0] }}"
  register: mon_secret_file

- debug: msg="{{ mon_secret_file['content'] | b64decode }}"

```
