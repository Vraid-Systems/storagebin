storagebin
============

django-nonrel based project for using Google App Engine as a REST-ish blobstore.

storagebin is based on the
[django-testapp](https://github.com/django-nonrel/django-testapp)
template for creating a Google App Engine app with
[django-nonrel](https://github.com/django-nonrel).
Run `./setup.sh APP_ID VERSION_ID` to initialize a development environment;
this will download all dependencies and generate an `app.yaml`.

For use with [storagebin_js](https://github.com/jzerbe/storagebin_js).

Development Dependencies
------------
- a standard [POSIX](http://en.wikipedia.org/wiki/POSIX#POSIX-oriented_operating_systems) shell
- [git](http://git-scm.com/downloads) and [hg](http://mercurial.selenic.com/wiki/Download) binaries in path

Tested Dev Environments
------------
- Cygwin (bash) on Windows 7 (64 bit)
- OSX 10.8.x (64 bit)

Development Commands
------------
- run unit tests: `python manage.py test storagebin`
- load example `BinOwner` for local manual testing: `python manage.py loaddata storagebin/fixtures/test_data.yaml`
- run local dev server: `python manage.py runserver`

Production Deploy
------------
1. deploy the project to GAE: `python manage.py deploy`. This could take 10
minutes. May want to wait a few more minutes after it finishes for the HRD
to stabilize.
2. Create the first owner by connecting to the remote datastore -
`python manage.py remote shell` - and executing the following with the remote
Python interpreter:

```python
from storagebin.models import BinOwner
bin_owner = BinOwner(email='example@example.com', key='example')
bin_owner.save()
```
