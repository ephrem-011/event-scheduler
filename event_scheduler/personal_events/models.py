from django.db import models
from user.models import User

class RecurrenceType(models.TextChoices):
    ONE_TIME = "one_time", "One-Time"
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    INTERVAL = "interval", "Every Nth Day/Week/Month"
    WEEKDAY = "weekday", "Weekday (e.g., every Monday)"
    RELATIVE = "relative", "Relative (e.g., every 2nd Monday of the month)"

class DayOrInterval(models.TextChoices):
    MONDAY = 'monday', 'Monday'
    TUESDAY = 'tuesday', 'Tuesday'
    WEDNESDAY = 'wednesday', 'Wednesday'
    THURSDAY = 'thursday', 'Thursday'
    FRIDAY = 'friday', 'Friday'
    SATURDAY = 'saturday', 'Saturday'
    SUNDAY = 'sunday', 'Sunday'
    WEEKDAY = 'weekday', 'Weekday'
    WEEKEND = 'weekend_day', 'Weekend day (Sat or Sun)'

class NthChoices(models.TextChoices):
    FIRST = 'first', 'First'
    SECOND = 'second', 'Second'
    THIRD = 'third', 'Third'
    LAST = 'last', 'Last'
    NTH = 'nth', 'Nth'
    
class GeneralTimeFrame(models.TextChoices):
    YEAR = 'year', "Year"
    MONTH = 'month', "Month"
    WEEK = 'week', "Week"
    DAY = 'day', "Day"

class RelativeTimeFrame(models.TextChoices):
    MONTH = 'month', 'Month'
    YEAR = 'year', 'Year'

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    event_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    recursion_type = models.CharField(
        max_length=150, 
        choices=RecurrenceType.choices, 
        default=RecurrenceType.ONE_TIME
    )

    # Optional fields for 'relative' recurrence type
    relative_n = models.CharField(
        max_length=100, 
        choices=NthChoices,
        null=True, 
        blank=True
    ) 
    relative_day_or_interval = models.CharField(
        max_length=100, 
        choices=DayOrInterval.choices, 
        null=True, 
        blank=True
    )  
    relative_timeframe = models.CharField(
        max_length=100, 
        choices=RelativeTimeFrame.choices,
        null=True, 
        blank=True
    )    

    # Optional fields for 'interval' recurrence type
    interval_n = models.IntegerField(null=True, blank=True)  
    interval_timeframe = models.CharField(
        max_length=150, 
        choices=GeneralTimeFrame.choices, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

class Dates_for_list_view(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')
    date = models.DateField()

class calendar_grid(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    date = models.IntegerField()
    day_of_week = models.IntegerField()
    day_rank_month = models.IntegerField()
    day_rank_year = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'month', 'date'], name='unique_date')
        ]