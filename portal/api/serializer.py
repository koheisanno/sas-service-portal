from rest_framework import serializers 
from datetime import datetime, timedelta
from django.utils import timezone
from portal.models import *
from .mixins import EagerLoadingMixin

class LinkSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Link 
        fields =  '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = UserProfile 
        fields =  '__all__'

class ClubTagSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Club 
        fields = ('tags',)

#TagListAPIView
class TagSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Tag
        fields = '__all__'

#RecordCreateAPIView, RecordDetailAPIView
class RecordSerializer(serializers.ModelSerializer): 
    user = serializers.StringRelatedField(read_only = True)
    club = serializers.StringRelatedField(read_only = True)
    checkInDate = serializers.DateField(format="%d/%m/%Y", read_only = True)

    class Meta: 
        model = Record
        fields = '__all__'

#EventBulkCreateAPIView, EventSeriesAPIView, EventDetailAPIView, 
class EventSerializer(serializers.ModelSerializer): 
    records = RecordSerializer(many = True, read_only = True)
    club = serializers.StringRelatedField(read_only = True)

    class Meta: 
        model = Event 
        fields = '__all__'

#ClubListAPIView, ClubDetailAPIView, ClubJoinLeaveAPIView
class ClubSerializer(serializers.ModelSerializer, EagerLoadingMixin): 
    select_related_fields = ('primary_contact',)
    prefetch_related_fields = ('members', 'officers', 'tags')

    tags = TagSerializer(many=True)
    is_member = serializers.SerializerMethodField()
    umbrella = serializers.SerializerMethodField()
    officers = UserSerializer(many=True)
    primary_contact = serializers.PrimaryKeyRelatedField(queryset = UserProfile.objects.all(), allow_null=True)

    def get_umbrella(self, obj):
        return obj.get_umbrella_display()
    
    def get_is_member(self, obj):
        if 'request' in self.context and self.context['request'].method == 'GET':
            request = self.context.get("request")
            if not request.user.is_authenticated:
                return False
            return obj.members.filter(pk=request.user.userProfile.pk).exists()

    class Meta:
        model = Club
        fields = '__all__'

#RecordUserCreateAPIView
class RecordCheckinSerializer(serializers.ModelSerializer): 
    user = serializers.StringRelatedField(read_only = True)
    club = serializers.StringRelatedField(read_only = True)

    class Meta: 
        model = Record  
        exclude = ("event","hours", "checkInDate", "name")

#HOME

class HomeEventSerializer(serializers.ModelSerializer): 
    club = serializers.PrimaryKeyRelatedField(read_only = True)
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    endTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta: 
        model = Event
        fields = '__all__'

class HomeClubSerializer(serializers.ModelSerializer): 
    events = HomeEventSerializer(many=True, read_only=True)

    class Meta: 
        model = Club 
        fields = ('id', 'events', 'name', 'logo', 'color_primary', 'color_secondary')

class HomeUserProfileSerializer(serializers.ModelSerializer):
    memberClubs = HomeClubSerializer(many = True, read_only = True)
    officerClubs = serializers.StringRelatedField(many = True, read_only = True)

    class Meta: 
        model = UserProfile 
        fields = '__all__'

#ClubCurrentEventsAPIView
class ClubCurrentEventsSerializer(serializers.ModelSerializer): 
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        time_change = timedelta(minutes=20)
        now = timezone.now()
        lowerBound = now-time_change
        upperBound = now+time_change
        currentEvents = obj.events.filter(startTime__lte=upperBound, endTime__gte=lowerBound)
        return  EventSerializer(currentEvents, many=True).data

    class Meta:
        model = Club
        fields = ('id', 'events', 'name',)

#OFFICER DATA SERIALIZERS

class OfficershipRecordSerializer(serializers.ModelSerializer): 
    user = UserSerializer(read_only = True)

    class Meta: 
        model = Record
        fields = '__all__'

class OfficershipEventSerializer(serializers.ModelSerializer):
    hours = serializers.ReadOnlyField()
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    endTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    records = OfficershipRecordSerializer(many=True) 

    class Meta:
        model = Event
        fields = '__all__'
        

class OfficershipUserProfileSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()

    def get_fullName(self, obj):
        return obj.firstName + " " + obj.lastName

    class Meta: 
        model = UserProfile
        exclude = ("user", "classOf",)


#UsersListAPIView
class OfficershipOfficersSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields= '__all__'

    #student or faculty
    def get_status(self, obj):
        for char in obj.email:
            if char.isdigit():
                return "student"
        return "faculty"

#OfficerClubAPIView
class OfficershipClubSerializer(serializers.ModelSerializer): 
    members = OfficershipUserProfileSerializer(many=True, read_only = True)
    officers = OfficershipOfficersSerializer(many = True, read_only = True)
    events = OfficershipEventSerializer(many = True, read_only = True)
    umbrella = serializers.SerializerMethodField()
    records = RecordSerializer(many=True, read_only = True)
    primary_contact = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Club
        fields= '__all__'

    def get_umbrella(self, obj):
        return obj.get_umbrella_display()


#OfficerClubAPIView
class OfficershipSerializer(serializers.ModelSerializer):
    officerClubs = OfficershipClubSerializer(many = True, read_only = True)
    
    class Meta: 
        model = UserProfile 
        fields = ['officerClubs']