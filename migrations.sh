#!/bin/bash 

# delete migrations
echo "Deleting migrations..."
rm -v app/migrations/000*

echo ""
echo "Making migrations..."
# make migatrions then migrate
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Loading fixtures..."
# load fixtuxes in order
python manage.py loaddata app/fixtures/initial_brands.yaml
python manage.py loaddata app/fixtures/initial_products.yaml
python manage.py loaddata app/fixtures/initial_batteries.yaml
python manage.py loaddata app/fixtures/initial_dimension_names.yaml
python manage.py loaddata app/fixtures/initial_panels.yaml
python manage.py loaddata app/fixtures/initial_appliances.yaml
python manage.py loaddata app/fixtures/*.yaml
