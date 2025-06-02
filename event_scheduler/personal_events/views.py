from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import date, timedelta
from django.views.generic import *
from personal_events.models import *
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from personal_events.serializers import *
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from personal_events.handle_recursion import handle_recursion

class CreateEvent(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def perform_create(self, serializer):
        my_event = serializer.save(user=self.request.user)
        handle_recursion(self.request.user, my_event)

class ListEvents(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventListSerializer    
    def get_queryset(self):
        return EventList.objects.filter(user = self.request.user)
             
class UpdateOrDeleteEvent(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def perform_update(self, serializer):
        updated_event = serializer.save()
        EventList.objects.filter (event = updated_event).delete()
        handle_recursion(self.request.user, updated_event)
    def perform_destroy(self, instance):
        if Event.objects.filter(date=instance.date).count() == 1:
            x = calendar_grid.objects.get(year = instance.date.year, month = instance.date.month, day = instance.date.day)
            x.is_booked = False
            x.save()
            return super().perform_destroy(instance)
        return super().perform_destroy(instance)
class DestroySpecificOccurrence(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EventList.objects.all()
    serializer_class = EventListSerializer

    def perform_destroy(self, instance):
        if EventList.objects.filter(date=instance.date).count() == 1:
            x = calendar_grid.objects.get(year = instance.date.year, month = instance.date.month, day = instance.date.day)
            x.is_booked = False
            x.save()
            return super().perform_destroy(instance)
        return super().perform_destroy(instance)
class CalendarGrid(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = calendar_grid.objects.all()
    serializer_class = CalendarGridSerializer

