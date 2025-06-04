from rest_framework import serializers
from personal_events.models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['user']
    def validate(self, attrs):
        instance = Event(**attrs)
        instance.clean()
        return attrs

class EventListSerializer(serializers.ModelSerializer):
    EventName = serializers.CharField(source = 'event.event_name')
    Time = serializers.CharField(source = 'event.time')
    class Meta:
        model = EventList
        fields = ['id', 'user', 'EventName', 'date', 'Time']

class CalendarGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar_grid
        fields = '__all__'