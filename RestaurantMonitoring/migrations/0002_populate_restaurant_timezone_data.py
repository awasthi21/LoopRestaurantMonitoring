# Generated by Django 4.1.7 on 2023-04-04 16:50

from django.db import migrations,transaction
from RestaurantMonitoring.commons import *
from .. import  restaurant_montioring_local_settings as  local
from RestaurantMonitoring.models import *

#populate the restaurant_data based on store_id_timezone csv

@transaction.atomic
def populate_restaurant_data_in_db(apps,schema_editor):
    
    store_id_timezone_data=CsvFileReader(local.RESTAURANT_TIMEZONE_CSV_URL,local.RESTAURANT_TIMEZONE_FILEPATH).get_data()
    restaurant_objs=[]
    for row in store_id_timezone_data:
        store_id=int(row["store_id"].strip())
        timezone_str=row["timezone_str"].strip()
        restaurant_objs.append(Restaurant(store_id=store_id,timezone_str=timezone_str))
    Restaurant.objects.bulk_create(restaurant_objs)
    print(len(restaurant_objs))
    
    
@transaction.atomic    
def reverse_populate_restaurant_data_in_db(apps, schema_editor):
    Restaurant.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantMonitoring', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_restaurant_data_in_db,reverse_code=reverse_populate_restaurant_data_in_db)
    ]