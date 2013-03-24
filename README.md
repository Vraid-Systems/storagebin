storagebin, a django-nonrel based Google App Engine app
=========================================================

django-nonrel based project for using Google App Engine as a REST-ish blobstore

storagebin is based on the [django-testapp](https://github.com/django-nonrel/django-testapp)
template for creating a Google App Engine app with [django-nonrel](https://github.com/django-nonrel).
Run `./setup.sh APP_ID VERSION_ID` to initialize a local development environment.

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
