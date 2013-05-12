storagebin
============

django-nonrel based project for using Google App Engine as a REST-ish blobstore

storagebin is based on the [django-testapp](https://github.com/django-nonrel/django-testapp)
template for creating a Google App Engine app with [django-nonrel](https://github.com/django-nonrel).
Run `./setup.sh APP_ID VERSION_ID` to initialize a development environment;
this will download all dependencies and generate an `app.yaml`.

Development Dependencies
------------
- a standard [POSIX](http://en.wikipedia.org/wiki/POSIX#POSIX-oriented_operating_systems) shell
- [git](http://git-scm.com/downloads) and [hg](http://mercurial.selenic.com/wiki/Download) binaries in path
- [pip](http://pypi.python.org/pypi/pip) binary in path

Gotchas
------------
- GitHub requires you to have the public-key of the cloning machine on file,
even when cloning from a public repository.

Tested Environments
------------
- Cygwin (bash) on Windows 7 (64 bit)
- Google App Engine Release 1.8.0

Development Server
------------
1. cd into the root of a cloned copy of this project
2. run: `python manage.py runserver`

Production Deploy
------------
1. cd into the root of a cloned copy of this project
2. deploy the project to GAE: `python manage.py deploy`. This could take 10
minutes. May want to wait a few more minutes after it finishes for the HRD
to stabilize.
3. Create the first owner by connecting to the remote datastore -
`python manage.py remote shell` - and executing the following with the remote
Python interpreter:

```python
from storagebin.models import Binary, BinOwner
bin_owner = BinOwner(email='example@example.com', key='example')
bin_owner.save()
```
