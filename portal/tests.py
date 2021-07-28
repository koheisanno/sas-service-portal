from django.test import TestCase

import secrets
# Create your tests here.
from .models import UserProfile, Club, Event, Record, Tag
from django.contrib.auth.models import User

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

for user in UserProfile.objects.all():
    for record in user.records.all():
        club = record.club
        club.members.add(user)