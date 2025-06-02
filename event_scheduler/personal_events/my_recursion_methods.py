from personal_events.models import *
from datetime import date, timedelta
from rest_framework import serializers
def perform_daily_recursion(user, event):
    start_date = event.date
    while start_date <= date(2030, 12, 31):
        booked_date = calendar_grid.objects.get(year = start_date.year, month = start_date.month, day = start_date.day)
        booked_date.is_booked = True
        booked_date.save()
        EventList.objects.create(user = user, event = event, date = start_date)
        start_date+= timedelta(days=1)
    
def perform_weekly_recursion(user, event):
    start_date = event.date
    while start_date <= date(2030,12,31):
        booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
        booked_date.is_booked = True
        booked_date.save()
        EventList.objects.create(user = user, event = event, date = start_date)
        start_date+= timedelta(days=7)
def perform_monthly_recursion(user, event):
    start_date = event.date
    while start_date <= date(2030,12,31):
        booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
        booked_date.is_booked = True
        booked_date.save()
        EventList.objects.create(user = user, event = event, date = start_date)
        start_date+= timedelta(days=30)

def perform_interval_recursion(user, event, ):
    start_date = event.date
    if event.interval_timeframe == 'day':
        while start_date <= date(2030,12,31):
            booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
            booked_date.is_booked = True
            booked_date.save()
            EventList.objects.create(user = user, event = event, date = start_date)
            start_date+= timedelta(days=event.interval_n)
    if event.interval_timeframe == 'week':
        interval = event.interval_n * 7
        while start_date <= date(2030,12,31):
            booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
            booked_date.is_booked = True
            booked_date.save()
            EventList.objects.create(user = user, event = event, date = start_date)
            start_date+= timedelta(days=interval)
    if event.interval_timeframe == 'month':
        interval = event.interval_n * 30
        while start_date <= date(2030,12,31):
            booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
            booked_date.is_booked = True
            booked_date.save()
            EventList.objects.create(user = user, event = event, date = start_date)
            start_date+= timedelta(days=interval)
    if event.interval_timeframe == 'year':
        interval = event.interval_n * 365
        while start_date <= date(2030,12,31):
            booked_date = calendar_grid.objects.get(year=start_date.year, month = start_date.month, day = start_date.day)
            booked_date.is_booked = True
            booked_date.save()
            EventList.objects.create(user = user, event = event, date = start_date)
            start_date+= timedelta(days=interval)

def perform_weekday_recursion(user, event):
    today = date.today()
    booked_dates = calendar_grid.objects.filter(full_date__gte=today, day_of_week = event.weekday_choice).order_by('year', 'month', 'day')
    first_occurence = booked_dates.first()
    first_occurence_weekday = date(first_occurence.year, first_occurence.month, first_occurence.day)
    event.date = first_occurence_weekday
    for d in booked_dates:
        d.is_booked = True
        d.save()
        real_date = date(d.year, d.month, d.day)
        EventList.objects.create(user = user, event = event, date = real_date)
def perform_relative_recursion(user, event):
    today = date.today()
    if event.relative_timeframe == 'month':
        rank_choice = event.relative_n
        day_choice = event.relative_day_or_interval
        if rank_choice == 'last':
            if day_choice == 'weekday':
                for d in calendar_grid.objects.values('year', 'month').order_by('year', 'month').distinct():
                    week_days = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(1,6), year = d['year'], month = d['month']).order_by('year', 'month', 'day')
                    last_day = week_days.last()
                    last_day.is_booked = True
                    last_day.save()
                    real_date = date(last_day.year, last_day.month, last_day.day)
                    EventList.objects.create(user = user, event = event, date = real_date)
                
            elif day_choice == 'weekend':
                for d in calendar_grid.objects.values('year', 'month').order_by('year', 'month').distinct():
                    week_ends = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(6,8), year = d['year'], month = d['month']).order_by('year', 'month', 'day')
                    last_day = week_ends.last()
                    last_day.is_booked = True
                    last_day.save()
                    real_date = date(last_day.year, last_day.month, last_day.day)
                    EventList.objects.create(user = user, event = event, date = real_date)
        else:
            if day_choice == 'weekday':
                for d in calendar_grid.objects.values('year', 'month').order_by('year', 'month').distinct():
                    week_days = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(1,6), year = d['year'], month = d['month']).order_by('year', 'month', 'day')
                    try:
                        booked_date = week_days[int(event.relative_n) - 1]
                        booked_date.is_booked = True
                        booked_date.save()
                        real_date = date(booked_date.year, booked_date.month, booked_date.day)
                        EventList.objects.create(user = user, event = event, date = real_date)
                    except IndexError:
                        raise serializers.ValidationError(f"There is no {event.relative_n}th weekday in the month. Try again")
            elif day_choice == 'weekend':
                for d in calendar_grid.objects.values('year', 'month').order_by('year', 'month').distinct():
                    week_ends = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(6,8), year = d['year'], month = d['month']).order_by('year', 'month', 'day')
                    try:
                        booked_date = week_ends[int(event.relative_n) - 1]
                        booked_date.is_booked = True
                        booked_date.save()
                        real_date = date(booked_date.year, booked_date.month, booked_date.day)
                        EventList.objects.create(user = user, event = event, date = real_date)
                    except IndexError:
                        raise serializers.ValidationError(f"There is no {event.relative_n}th weekend day in the month. try again")
            else:
                booked_dates = calendar_grid.objects.filter(day_rank_month = int(event.relative_n), day_of_week = int(event.relative_day_or_interval)).order_by('year', 'month', 'day')
                if len(booked_dates) > 0:                    
                    for d in booked_dates:
                        d.is_booked = True
                        d.save()
                        EventList.objects.create(user=user, event = event, date = d.full_date)
                else:
                    raise serializers.ValidationError(f"There is no {event.relative_n}th {DayOrInterval(event.relative_day_or_interval).label} in the month")
    if event.relative_timeframe == 'year':    
        rank_choice = event.relative_n
        day_choice = event.relative_day_or_interval
        if rank_choice == 'last':
            if day_choice == 'weekday':
                for y in calendar_grid.objects.values('year').order_by('year').distinct():
                    week_days = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(1,6), year = y['year']).order_by('year', 'month', 'day')
                    last_day = week_days.last()
                    last_day.is_booked = True
                    last_day.save()
                    real_date = date(last_day.year, last_day.month, last_day.day)
                    EventList.objects.create(user = user, event = event, date = real_date)

            elif day_choice == 'weekend':
                for y in calendar_grid.objects.values('year').order_by('year').distinct():
                    week_ends = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(6,8), year = y['year']).order_by('year', 'month', 'day')
                    last_day = week_ends.last()
                    last_day.is_booked = True
                    last_day.save()
                    real_date = date(last_day.year, last_day.month, last_day.day)
                    EventList.objects.create(user = user, event = event, date = real_date)
        else:
            if day_choice == 'weekday':
                for y in calendar_grid.objects.values('year').order_by('year').distinct():
                    week_days = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(1,6), year = y['year']).order_by('year', 'month', 'day')
                    try:
                        booked_date = week_days[int(event.relative_n) - 1]
                        booked_date.is_booked = True
                        booked_date.save()
                        real_date = date(booked_date.year, booked_date.month, booked_date.day)
                        EventList.objects.create(user = user, event = event, date = real_date)
                    except IndexError:
                        raise serializers.ValidationError (f"There is no {event.relative_n}th weekday in the year. Try again")
            elif day_choice == 'weekend':
                for y in calendar_grid.objects.values('year').order_by('year').distinct():
                    week_ends = calendar_grid.objects.filter(full_date__gte=today, day_of_week__in = range(6,8), year = y['year']).order_by('year', 'month', 'day')
                    try:
                        booked_date = week_ends[int(event.relative_n) - 1]
                        booked_date.is_booked = True
                        booked_date.save()
                        real_date = date(booked_date.year, booked_date.month, booked_date.day)
                        EventList.objects.create(user = user, event = event, date = real_date)
                    except IndexError:
                        raise serializers.ValidationError(f"There is no {event.relative_n}th weekend day in the year. Try again")
            else:
                try:
                    booked_date = calendar_grid.objects.filter(day_rank_year = int(event.relative_n), day_of_week = int(event.relative_day_or_interval))
                    for d in booked_date:
                        d.is_booked = True
                        d.save()
                        EventList.objects.create(user=user, event = event, date = d.full_date)
                except calendar_grid.DoesNotExist:
                    raise ValidationError(f"There is no {event.relative_n}th {DayOrInterval(event.relative_day_or_interval).label} in the year")
def perform_one_time(user, event):
    event_date = event.date
    booked_date = calendar_grid.objects.get(year=event_date.year, month = event_date.month, day = event_date.day)
    booked_date.is_booked = True
    booked_date.save()
    EventList.objects.create(user = user, event = event, date = event_date)





        


