from django.test import TestCase

# Create your tests here.
from .models import UserProfile, Club, Event, Record, Tag

umbrellas = {
  "Education for All": 'ED4ALL',
  "Global Issues": 'GI',
  "SAS-Centric": 'SASCENTRIC',
  "Help for the Disabled and Ill":'H4DI',
  "Poverty Eradication":'PE',
  "New Service Club":'NSC',
  "Service Project":'SP'
}

import csv

with open('/Users/koheisanno/Documents/SASServicePortal/ServicePortal/portal/SAS_Service_Portal_Database_2.0.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            Club(name=row[0], umbrella=umbrellas[row[1]], mission=row[4], description="Default", color_primary=row[5], color_secondary=row[6]).save()
            line_count += 1
    print(f'Processed {line_count} lines.')