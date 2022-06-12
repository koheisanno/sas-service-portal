from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.contrib.postgres.fields import HStoreField
from datetime import datetime

from colorfield.fields import ColorField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfile")

    classOf = models.PositiveIntegerField(null=True, blank=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    hours = HStoreField(blank=True, null=True)

    class Meta:
        ordering = ['firstName']

    def __str__(self):
        return self.firstName + " " + self.lastName

    def update_hours(self):
        hours_dict = {}
        records = self.records.all()
        for record in records:
            if record.club.name in hours_dict:
                hours_dict[record.club.name]+=record.hours
            else:
                hours_dict[record.club.name]=record.hours

        self.hours = hours_dict
        self.save()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Club(models.Model):

    EDUCATION_FOR_ALL = 'ED4ALL'
    GLOBAL_ISSUES = 'GI'
    SAS_CENTRIC = 'SASCENTRIC'
    HELP_FOR_DISABLED_AND_ILL = 'H4DI'
    POVERTY_ERADICATION = 'PE'
    NEW_SERVICE_CLUBS = 'NSC'

    UMBRELLA_CHOICES = (
        (EDUCATION_FOR_ALL, 'Education for All'),
        (GLOBAL_ISSUES, 'Global Issues'),
        (SAS_CENTRIC, 'SAS-Centric'),
        (HELP_FOR_DISABLED_AND_ILL, 'Help for the Disabled and Ill'),
        (POVERTY_ERADICATION, 'Poverty Eradication'),
        (NEW_SERVICE_CLUBS, 'New Service Clubs')
    )


    name = models.CharField(max_length=500, unique=True)
    mission = models.CharField(max_length=200)
    description = models.CharField(max_length=1200, null=True, blank=True)
    involvement = models.CharField(max_length=400, null=True, blank=True)
    welcome = models.CharField(max_length=800)
    meeting = models.CharField(max_length=200)
    members = models.ManyToManyField(UserProfile, blank=True, related_name="memberClubs")
    officers = models.ManyToManyField(UserProfile, blank=True, related_name="officerClubs")
    umbrella = models.CharField(max_length=200, choices=UMBRELLA_CHOICES)
    color_primary = ColorField(default='#FFFFFF')
    color_secondary = ColorField(default='#1A1A1A')
    tags = models.ManyToManyField('Tag', related_name='clubs', blank=True)
    primary_contact = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="primary_contact_club", null=True, blank=True)
    instagram = models.CharField(max_length=150, null=True, blank=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    startTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    endTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=50)
    series = models.UUIDField(blank=True, null=True)
    location = models.CharField(max_length=50)
    hours = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['startTime']


    def __str__(self):
        return self.name + " - " + self.club.name

class Record(models.Model):
    checkInDate = models.DateField(default=date.today)
    name = models.CharField(max_length=50, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="records")
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="records")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="records")
    hours = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-checkInDate']

    def __str__(self):
        return self.club.name + ": " + self.user.firstName + " " + self.user.lastName


class Link(models.Model):
    CATEGORY_CHOICES = (
        ('quick-links', 'Quick Links'),
        ('officers-only', 'Officers Only'),
    )

    name = models.CharField(max_length=120)
    url = models.CharField(max_length=120)
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.name