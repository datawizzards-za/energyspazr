#!/bin/bash 

MIGS=$1

#Comment OPTIONS in forms
echo "Commenting OPTIONS in froms.py"
sed -i 's/OPTIONS = ((p.name, p.name) for p in models.Appliance.objects.all())/#OPTIONS = ((p.name, p.name) for p in models.Appliance.objects.all())/' app/forms.py
sed -i 's/name = forms.ChoiceField(choices=OPTIONS, required=True)/#name = forms.ChoiceField(choices=OPTIONS, required=True)/' app/forms.py

# delete migrations
echo "Deleting migrations..."
rm -v app/migrations/000*

echo ""
echo "Making migrations..."
echo "make migatrions then migrate"
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Loading fixtures..."
# load fixtuxes in order

for mig in `cat $MIGS`; do
    python manage.py loaddata $mig;
    done

#UnComment OPTIONS in forms
echo "Uncommenting OPTIONS in froms.py"
sed -i 's/#OPTIONS = ((p.name, p.name) for p in models.Appliance.objects.all())/OPTIONS = ((p.name, p.name) for p in models.Appliance.objects.all())/' app/forms.py
sed -i 's/#name = forms.ChoiceField(choices=OPTIONS, required=True)/name = forms.ChoiceField(choices=OPTIONS, required=True)/' app/forms.py

echo ""
echo "DONE!"
