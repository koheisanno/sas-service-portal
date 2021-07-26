from django.urls import path
from .views import *

urlpatterns = [
    path("user/", CurrentUserProfileAPIView.as_view(), name="current-user"), #user
    path("user-list/", UsersListAPIView.as_view(), name="user-list"), #add officer
    path("officer-list/", OfficersListAPIView.as_view(), name="officer-list"), #add officer
    path("officerships/", OfficershipAPIView.as_view(), name="current-user-officerships"), #officer dashboard
    path("club/", ClubListAPIView.as_view(), name="club-list"), #club search
    path("club/<int:pk>/", ClubDetailAPIView.as_view(), name="club-detail"), #get club data
    path("club/<int:pk>/logo/", ClubLogoAPIView.as_view(), name="club-logo"), #update club logo
    path("club/<int:pk>/current-events/", ClubCurrentEventsAPIView.as_view(), name="club-current-events"), #check-in page
    path("club/<int:pk>/remove-officer/", RemoveOfficerAPIView.as_view(), name="club-remove-officer"), #remove officer
    path("club/<int:pk>/add-officer/", AddOfficerAPIView.as_view(), name="club-add-officer"), #add officer
    path("club/<int:pk>/membership/", ClubJoinLeaveAPIView.as_view(), name="club-membership"), #POST DELETE membership
    path("club/<int:club_pk>/event/", EventBulkCreateAPIView.as_view(), name="event-create"), #bulk create club events
    path("event/delete/", EventBulkDeleteAPIView.as_view(), name="event-delete"), #delete events
    path("event/series/<int:pk>/<uuid:series_id>/<str:option>/", EventSeriesAPIView.as_view(), name="event-series"), #edit series events
    path("event/<int:pk>/", EventDetailAPIView.as_view(), name="event-detail"), #edit event
    path("event/<int:event_pk>/checkin/", RecordUserCreateAPIView.as_view(), name="event-checkin"), #checkin thru qr code
    path("record/", RecordCreateAPIView.as_view(), name="record-create"), #create single record
    path("record/<int:pk>/", RecordDetailAPIView.as_view(), name="record-detail"), #update single misc record using patch
    path("record/delete/", RecordBulkDeleteAPIView.as_view(), name="record-delete"), #delete records
    path("tag/", TagListAPIView.as_view(), name="tag-list"), #get tags
    path("link/", LinkAPIView.as_view(), name="links-list"), #get links


    path("profile/", UserProfileListCreateAPIView.as_view(), name="profile-list"),
    path("clubs-hour/<int:pk>/", ClubHoursAPIView.as_view(), name="club-hours-detail"),
    path("event/", EventListCreateAPIView.as_view(), name="event-list"),
]
