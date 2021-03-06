from django.shortcuts import render
import datetime

from rest_framework.generics import (
ListAPIView,
RetrieveAPIView,
RetrieveUpdateAPIView,
DestroyAPIView,
CreateAPIView,
)
from events.models import Event ,Booking
from .serializers import(
EventListSerializer,
EventDetailSerializer,
EventCreateUpdateSerializer,
UserLoginSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request):
 		my_data = request.data
 		serializer = UserLoginSerializer(data=my_data)
 		if serializer.is_valid(raise_exception=True):
  			valid_data = serializer.data
  			return Response(valid_data, status=HTTP_200_OK)
 		return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class UpcomingEventList(ListAPIView):
	current_date = datetime.date.today()
	queryset = Event.objects.filter(date__gte=current_date)
	serializer_class = EventListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter, OrderingFilter,]
	search_fields = ['title', 'description',]


class OrganizerEventList(ListAPIView):
	serializer_class = EventListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter, OrderingFilter,]
	search_fields = ['title', 'description',]

def get_queryset(self):
	return self.request.user.events.all()



# # ???????????????????????? NOT COMPLETED ????????????????????
# class BookedEventList(ListAPIView):
#  serializer_class = EventListSerializer
#  permission_classes = [AllowAny,]
#  filter_backends = [SearchFilter, OrderingFilter,]
#  search_fields = ['title', 'description',]

#  def get_queryset(self):
#   return self.request.user.events.all()
# # ????????????????????????????????????????????????????????????




class EventDetail(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [AllowAny,]

class EventCreate(CreateAPIView):
	serializer_class = EventDetailSerializer
	permission_classes = [IsAuthenticated,]

def perform_create(self, serializer):
	serializer.save(organizer=self.request.user)

class EventUpdate(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsOrganizer,]

class EventDelete(DestroyAPIView):
	queryset = Event.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsOrganizer,]