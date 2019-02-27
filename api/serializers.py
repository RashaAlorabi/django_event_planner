from rest_framework import serializers
from events.models import (Event, Booking) 
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', ]


class BookingSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Booking
		fields = ['user']


class EventListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
			view_name = 'api-detail',
			lookup_field = 'id',
			lookup_url_kwarg = 'event_id',
		)
	class Meta:
		model = Event
		fields = ['id', 'title','date' ,'detail']


class OrganizerEventListSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    events = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = 'events','organizer'

    def get_events(self, obj):
        events = Event.objects.filter(events=obj)
        events_list = EventListSerializer(events, many=True).data
        return events_list


class EventDetailSerializer(serializers.ModelSerializer):
	organizer = UserSerializer()

	class Meta:
		model = Event
		fields = '__all__'


class EventCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['organizer',]
