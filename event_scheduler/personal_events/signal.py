from datetime import date, timedelta
from personal_events.models import calendar_grid

def populate_dates(start_year=2025, end_year=2030):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    current_date = start_date
    bulk_create_list = []

    while current_date <= end_date:
        bulk_create_list.append(calendar_grid(
            year = current_date.year,
            month = current_date.month,
            date = current_date.day,
            day_of_week = current_date.isoweekday()
        ))
        current_date += timedelta(days=1)

    calendar_grid.objects.bulk_create(bulk_create_list, ignore_conflicts=True)

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for weekday in range(1, 8):
                dates = calendar_grid.objects.filter(year=year, month=month, day_of_week=weekday).order_by('year', 'month', 'date')
                rank = 1
                for d in dates:
                    d.day_rank_month = rank
                    d.save()
                    rank +=1

    for year in range(start_year, end_year + 1):
        for weekday in range(1, 8):
            dates = calendar_grid.objects.filter(year=year, day_of_week=weekday).order_by('year', 'month', 'date')
            rank = 1
            for d in dates:
                d.day_rank_year = rank
                d.save()
                rank += 1


if __name__ == "__main__":
    populate_dates()