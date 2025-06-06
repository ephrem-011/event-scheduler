from django.db import models
from user.models import User
from datetime import date
from django.core.exceptions import ValidationError


class RecurrenceType(models.TextChoices):
    ONE_TIME = "one_time", "One-Time"
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    INTERVAL = "interval", "Every Nth Day/Week/Month"
    WEEKDAY = "weekday", "Weekday (e.g., every Monday)"
    RELATIVE = "relative", "Relative (e.g., every 2nd Monday of the month)"

class DayOrInterval(models.TextChoices):
    MONDAY = '1', 'Monday'
    TUESDAY = '2', 'Tuesday'
    WEDNESDAY = '3', 'Wednesday'
    THURSDAY = '4', 'Thursday'
    FRIDAY = '5', 'Friday'
    SATURDAY = '6', 'Saturday'
    SUNDAY = '7', 'Sunday'
    WEEKDAY = 'weekday', 'Weekday'
    WEEKEND = 'weekend', 'Weekend day (Sat or Sun)'

class WeekdayChoices(models.IntegerChoices):
    MONDAY = 1, 'Monday'
    TUESDAY = 2, 'Tuesday'
    WEDNESDAY = 3, 'Wednesday'
    THURSDAY = 4, 'Thursday'
    FRIDAY = 5, 'Friday'
    SATURDAY = 6, 'Saturday'
    SUNDAY = 7, 'Sunday'
    
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

    # Options for 'relative' recurrence type
    relative_n = models.CharField(
        max_length=100, 
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

    # Options for 'interval' recurrence type
    interval_n = models.IntegerField(null=True, blank=True)  
    interval_timeframe = models.CharField(
        max_length=150, 
        choices=GeneralTimeFrame.choices, 
        null=True, 
        blank=True
    )

    # Options for 'weekday' recurrence type
    weekday_choice = models.IntegerField(
        choices=WeekdayChoices.choices, 
        null=True, 
        blank=True
    )

    from django.core.exceptions import ValidationError

    def clean(self):
        super().clean()
        if self.recursion_type not in ['relative', 'weekday'] and not self.date:
            raise ValidationError({'date': "This field is required for the selected recurrence type."})
        if self.recursion_type == RecurrenceType.INTERVAL:
            if not (self.interval_n and self.interval_timeframe):
                raise ValidationError("All interval fields must be set when recurrence type is 'interval'.")
        else:
            if self.interval_n or self.interval_timeframe:
                raise ValidationError("Intervals fields must be empty unless recurrence type is 'interval'.")

        if self.recursion_type == RecurrenceType.WEEKDAY:
            if not (self.weekday_choice):
                raise ValidationError("Day be set when recurrence type is 'weekday'.")
        else:
            if self.weekday_choice:
                raise ValidationError("Day shouldn't be set unless recurrence type is 'weekday'.")

        if self.recursion_type == RecurrenceType.RELATIVE:
            if not (self.relative_n and self.relative_day_or_interval and self.relative_timeframe):
                raise ValidationError("All relative fields must be set when recurrence type is 'relative'.")
        else:
            if self.relative_n or self.relative_day_or_interval or self.relative_timeframe:
                raise ValidationError("Relative fields must be empty unless recurrence type is 'relative'.")
                
        if not date(2025, 1, 1) <= self.date <= date(2030, 12, 31):
            raise ValidationError("Date must be between 2025 and 2030.")
        if not self.event_name:
            raise ValidationError("Event name cannot be empty")
        if not self.date:
            raise ValidationError("Date cannot be empty") 
        if not self.time:
            raise ValidationError("Time name cannot be empty")

class EventList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='occurrences')
    date = models.DateField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'event', 'date'], name='unique_event')]

class calendar_grid(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    full_date = models.DateField(null=True)
    day_of_week = models.IntegerField()
    day_rank_month = models.IntegerField(null=True, blank=True)
    day_rank_year = models.IntegerField(null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['full_date'], name='unique_full_date')]

