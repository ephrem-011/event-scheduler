from datetime import date, timedelta
from personal_events.models import calendar_grid
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def populate_dates (sender, **kwargs):
    start_date = date(2025, 1, 1)
    end_date = date(2030, 12, 31)
    current_date = start_date
    bulk_create_list = []

    while current_date <= end_date:
        bulk_create_list.append(calendar_grid(
            year = current_date.year,
            month = current_date.month,
            day = current_date.day,
            full_date = date(current_date.year, current_date.month,current_date.day),
            day_of_week = current_date.isoweekday()
        ))
        current_date += timedelta(days=1)

    calendar_grid.objects.bulk_create(bulk_create_list, ignore_conflicts=True)

    for year in range(2025, 2031):
        for month in range(1, 13):
            for weekday in range(1, 8):
                dates = calendar_grid.objects.filter(year=year, month=month, day_of_week=weekday).order_by('year', 'month', 'day')
                rank = 1
                for d in dates:
                    d.day_rank_month = rank
                    d.save()
                    rank +=1

    for year in range(2025, 2031):
        for weekday in range(1, 8):
            dates = calendar_grid.objects.filter(year=year, day_of_week=weekday).order_by('year', 'month', 'day')
            rank = 1
            for d in dates:
                d.day_rank_year = rank
                d.save()
                rank += 1


if __name__ == "__main__":
    populate_dates()