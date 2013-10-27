#!/bin/sh

if [ $# -lt 2 ]
then
    echo "usage: $0 APP_ID VERSION_ID"
    exit 1
fi

echo APP_ID will be set to: $1
echo VERSION_ID will be set to: $2

cat app_template.yaml | sed -e 's/application: REPLACE_ME/application: '$1'/g' > app.yaml
cat app.yaml | sed -e 's/version: REPLACE_ME/version: '$2'/g' > app.yaml

mkdir -p build
cd build

git clone https://github.com/django-nonrel/django.git
git clone https://github.com/django-nonrel/django-dbindexer.git
git clone https://github.com/django-nonrel/djangoappengine.git
git clone https://github.com/django-nonrel/djangotoolbox.git
hg clone https://bitbucket.org/twanschik/django-autoload

cd ..

rm -fr django
rm -fr dbindexer
rm -fr djangoappengine
rm -fr djangotoolbox
rm -fr autoload

cp -r build/django/django ./django
cp -r build/django-dbindexer/dbindexer ./dbindexer
cp -r build/djangoappengine/djangoappengine ./djangoappengine
cp -r build/djangotoolbox/djangotoolbox ./djangotoolbox
cp -r build/django-autoload/autoload ./autoload

rm -fr build
