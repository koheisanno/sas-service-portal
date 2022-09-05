from django.test import TestCase

import secrets
# Create your tests here.
from .models import UserProfile, Club, Event, Record, Tag
from django.contrib.auth.models import User