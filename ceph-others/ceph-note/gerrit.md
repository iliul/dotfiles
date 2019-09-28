```
pip install git-review
git remote set-url gerrit https://<username>:<http-password>@review.openstack.org/openstack/nova.gi
git review -s
git remote update
git checkout master
git pull --ff-only origin master
git review
```
