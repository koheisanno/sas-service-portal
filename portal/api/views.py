from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db import connection

from django.core.mail import send_mail
from django.conf import settings

from .mixins import CreateListMixin
from .permissions import EventIsOfficer, checkIsOfficer, IsOfficer, IsOfficerOrReadOnly
from portal.models import *
from .serializer import *

from django.db import connection, reset_queries
import time
import functools

#debug helper
def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()
        
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func

#get links
class LinkAPIView(APIView):

    def get(self, request):
        serializer = LinkSerializer(Link.objects.all(), many=True)
        return Response(serializer.data)

#get is authenticated
class CurrentUserAuthAPIView(APIView):
    def get(self, request):
        return Response(request.user.is_authenticated)

#get/update user profile
class CurrentUserProfileAPIView(APIView):

    def patch(self, request):
        serializer = HomeUserProfileSerializer(request.user.userProfile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = HomeUserProfileSerializer(request.user.userProfile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.is_authenticated:
            user = UserProfile.objects.prefetch_related(
                'memberClubs__events', 'memberClubs__events__club',
            ).get(pk=request.user.userProfile.pk)
            serializer = HomeUserProfileSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

#get officers only
class OfficersListAPIView(APIView):

    def get(self, request):
        queryset = UserProfile.objects.exclude(officerClubs=None)
        serializer = OfficershipOfficersSerializer(queryset, many=True)
        return Response(serializer.data)

#get all users
class UsersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = UserProfile.objects.all()
        serializer = OfficershipOfficersSerializer(queryset, many=True)
        return Response(serializer.data)

#get clubs
class ClubListAPIView(APIView):
    filter_backends = [SearchFilter,]
    search_fields = ["name"]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = ClubSerializer.setup_eager_loading(Club.objects.all())
        umbrellas = self.request.query_params.get("umbrella", None)
        nameQuery = self.request.query_params.get("search", None)
        if umbrellas is not None:
            umbrellas = umbrellas.split(",")
            queryset = queryset.filter(umbrella__in=umbrellas)
        if nameQuery is not None:
            queryset = queryset.filter(name__icontains=nameQuery)
        tags = self.request.query_params.get("tag", None)
        if tags is not None:
            tags = tags.split(",")
            for tag in tags:
                queryset = queryset.filter(tags__id=tag)
        serializer = ClubSerializer(queryset, many=True)
        return Response(serializer.data)

#post new events
class EventBulkCreateAPIView(CreateListMixin, generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        club_pk = self.kwargs.get("club_pk")
        club = get_object_or_404(Club, pk = club_pk)
        checkIsOfficer(self.request, club)

        serializer.save(club=club)

#delete/post club membership
class ClubJoinLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        club = get_object_or_404(Club, pk=pk)
        userProfile = request.user.userProfile
        
        club.members.remove(userProfile)

        if userProfile in club.officers.all():
            club.officers.remove(userProfile)

        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk):
        club = get_object_or_404(Club, pk=pk)
        userProfile = request.user.userProfile

        if userProfile not in club.members.all():     
            club.members.add(userProfile)

        subject = "Welcome to " + club.name + "!"
        message = "You joined " + club.name + " on the Service Portal.\n\n" + club.welcome
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [userProfile.email,]
        send_mail( subject, message, email_from, recipient_list )

        return Response(status=status.HTTP_200_OK)

#post remove officer
class RemoveOfficerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        club = get_object_or_404(Club, pk=pk)
        checkIsOfficer(self.request, club)

        officers_to_delete = UserProfile.objects.filter(id__in=request.data)

        club.officers.remove(*officers_to_delete)

        return Response(status=status.HTTP_204_NO_CONTENT)

class AddOfficerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        userprofile_pk = request.data

        club = get_object_or_404(Club, pk=pk)
        checkIsOfficer(self.request, club)

        club.officers.add(UserProfile.objects.get(id=userprofile_pk))

        if not club.members.filter(id=userprofile_pk).exists():
            club.members.add(UserProfile.objects.get(id=userprofile_pk))

        return Response(status=status.HTTP_204_NO_CONTENT)

class ClubDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsOfficerOrReadOnly]

class ClubTagAPIView(generics.RetrieveUpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubTagSerializer
    permission_classes = [IsOfficerOrReadOnly]
    

class ClubCurrentEventsAPIView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubCurrentEventsSerializer
    permission_classes = [IsAuthenticated]


class EventSeriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_pk=self.kwargs.get("pk")
        event=get_object_or_404(Event, pk=event_pk)
        checkIsOfficer(self.request, event.club)
        
        return event

    def formatDate(self, date):
        m = date.month
        d = date.day
        if m<10:
            m="0"+str(m)
        else:
            m=str(m)
        if d<10:
            d="0"+str(d)
        else:
            d=str(d)
        return str(date.year)+"-"+m+"-"+d


    def get(self, request, *args, **kwargs):
        event = self.get_object()
        checkIsOfficer(self.request, event.club)

        series_id = self.kwargs.get("series_id")

        events = Event.objects.filter(series = series_id, startTime__gte = event.startTime)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    
    def delete(self, request, *args, **kwargs):
        option = self.kwargs.get("option")
        event = self.get_object()
        checkIsOfficer(self.request, event.club)

        series_id = self.kwargs.get("series_id")

        if option=="all":
            events = Event.objects.filter(series = series_id)
        else:
            events = Event.objects.filter(series = series_id, startTime__gte = event.startTime)

        if events.count() > 0:
           [event.delete() for event in events]
           return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request, *args, **kwargs):
        edited_events = []

        option = self.kwargs.get("option")
        series_id = self.kwargs.get("series_id")
        event_pk = self.kwargs.get("pk")

        event = self.get_object()
        checkIsOfficer(self.request, event.club)
        data = request.data.copy()
        data["startTime"] = data.get("date") + " " + data.get("startTime")
        data["endTime"] = data.get("date") + " " + data.get("endTime")
        del data["date"]
        serializer = EventSerializer(event, data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        edited_events.append(event_pk)
        
        if option=="all":
            events = Event.objects.filter(series = series_id).exclude(pk = event_pk)
        else:
            events = Event.objects.filter(series = series_id, startTime__gte = event.startTime).exclude(pk = event_pk)

        name=request.data.get("name")
        location=request.data.get("location")
        hours=request.data.get("hours")
        date = request.data.get("date")
        startTime = request.data.get("startTime")
        endTime = request.data.get("endTime")

        for event in events:
            formattedDate = self.formatDate(event.startTime)
            data = {
                "name": name,
                "location": location,
                "hours": hours,
                "startTime": formattedDate+" "+startTime,
                "endTime": formattedDate+" "+endTime
            }

            serializer = EventSerializer(event, data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            edited_events.append(event.id)

        return Response(edited_events, status=status.HTTP_200_OK)

class EventBulkDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data

        event = get_object_or_404(Event, pk=ids[0])
        checkIsOfficer(self.request, event.club)

        Event.objects.filter(id__in=ids).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventIsOfficer]

#check-in
class RecordUserCreateAPIView(APIView):
    queryset = Record.objects.all()
    serializer_class = RecordCheckinSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_pk = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, pk=event_pk)
        
        club = event.club
        user = self.request.user.userProfile
        hours = event.hours

        if not user in club.members.all():
            club.members.add(user)

        record_queryset = Record.objects.filter(event=event, club=club, user=user)

        if record_queryset.exists():
            return Response("You have already checked into this event!", status=status.HTTP_200_OK)

        record = Record(event=event, club=club, user=user, hours=hours)
        record.save()

        return Response("Check-in successful.", status=status.HTTP_200_OK)
        

class OfficershipAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserProfile.objects.prefetch_related(
            'officerClubs__tags', 'officerClubs__events__records', 'officerClubs__events__records__user', 'officerClubs__members__records', 'officerClubs__officers', 'officerClubs__records', 'officerClubs__records__user', 'officerClubs__records__club',
        ).get(pk=request.user.userProfile.pk)
        serializer = OfficershipSerializer(user)
        return Response(serializer.data)


class RecordCreateAPIView(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event=None
        club=None
        userprofile=None

        if "event" in self.request.data:
            event_pk = self.request.data.get("event")
            event = get_object_or_404(Event, pk=event_pk)

        if "club" in self.request.data:
            club_pk = self.request.data.get("club")
            club = get_object_or_404(Club, pk=club_pk)

            checkIsOfficer(self.request, club)

        if "userprofile" in self.request.data:
            userprofile_pk = self.request.data.get("userprofile")
            userprofile = get_object_or_404(UserProfile, pk=userprofile_pk)

        serializer.save(club=club, user=userprofile, event=event)


class RecordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated, EventIsOfficer]


class RecordBulkDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data

        record = get_object_or_404(Record, pk=ids[0])
        checkIsOfficer(self.request, record.club)

        Record.objects.filter(id__in=ids).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()