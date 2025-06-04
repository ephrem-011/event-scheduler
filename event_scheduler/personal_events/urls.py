from django.urls import path
from personal_events import views
from django.contrib.auth.views import *

urlpatterns = [
    
    path('api/create', views.CreateEvent.as_view(), name='create_event'),
    path('api/events', views.ListEvents.as_view(), name='list_events'),
    path('api/events_on_specific_day/<str:date>', views.SpecificDateEvents.as_view(), name="specific_date_events"),
    path('api/update/<pk>', views.UpdateOrDeleteEvent.as_view(), name='update_event'),
    path('api/delete/<int:pk>/', views.UpdateOrDeleteEvent.as_view(), name='delete_event'),
    path('api/delete_occurence/<pk>/', views.DestroySpecificOccurrence.as_view(), name='delete_occurence'),
    path('api/calendar/', views.Calendar.as_view(), name='calendar')
    
]