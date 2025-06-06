from datetime import date, timedelta
from personal_events.models import calendar_grid
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection


@receiver(post_migrate)
def populate_dates (sender, **kwargs):
    print("Starting date population...")

    start_date = date(2025, 1, 1)
    end_date = date(2030, 12, 31)
    current_date = start_date
    bulk_create_list = []

    while current_date <= end_date:
            bulk_create_list.append(calendar_grid(
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
                full_date=current_date,
                day_of_week=current_date.isoweekday()
            ))
            current_date += timedelta(days=1)

    calendar_grid.objects.bulk_create(bulk_create_list, ignore_conflicts=True)
    print(f"Inserted {len(bulk_create_list)} dates.")

        # Step 2: Run raw SQL to update rankings fast
    with connection.cursor() as cursor:
        print("Updating day_rank_month using raw SQL...")
        cursor.execute('''
                UPDATE personal_events_calendar_grid AS c
                JOIN (
                    SELECT id,
                           ROW_NUMBER() OVER (PARTITION BY year, month, day_of_week ORDER BY day) AS rank_month
                    FROM personal_events_calendar_grid
                    WHERE year BETWEEN 2025 AND 2030
                ) AS ranked ON c.id = ranked.id
                SET c.day_rank_month = ranked.rank_month;
            ''')

        print("Updating day_rank_year using raw SQL...")
        cursor.execute('''
                UPDATE personal_events_calendar_grid AS c
                JOIN (
                    SELECT id,
                           ROW_NUMBER() OVER (PARTITION BY year, day_of_week ORDER BY month, day) AS rank_year
                    FROM personal_events_calendar_grid
                    WHERE year BETWEEN 2025 AND 2030
                ) AS ranked ON c.id = ranked.id
                SET c.day_rank_year = ranked.rank_year;
            ''')

        print("Finished updating rankings.")

if __name__ == "__main__":
    populate_dates()