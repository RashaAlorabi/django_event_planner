from django.shortcuts import render
import datetime

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from events.models import Event
from .serializers import(
	EventListSerializer,
	OrganizerEventListSerializer,
	EventDetailSerializer,
	EventCreateUpdateSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import SearchFilter, OrderingFilter

class UpcomingEventList(ListAPIView):
	current_date = datetime.date.today()
	queryset = Event.objects.filter(date__gte=current_date)
	serializer_class = EventListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter, OrderingFilter,]
	search_fields = ['title', 'description',]


# class OrganizerEventList(ListAPIView):
# 	queryset = Event.objects.all()
# 	serializer_class = OrganizerEventListSerializer
# 	permission_classes = [AllowAny,]
# 	filter_backends = [SearchFilter, OrderingFilter,]
# 	search_fields = ['title', 'description',]

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
