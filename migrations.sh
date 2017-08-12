#!/bin/bash 

MIGS=$1

# delete migrations
echo "Deleting migrations..."
rm -v app/migrations/000*

echo ""
echo "Making migrations..."
make migatrions then migrate
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Loading fixtures..."
# load fixtuxes in order

for mig in `cat $MIGS`; do
    python manage.py loaddata $mig;
    done

echo "DONE!"