from personal_events.my_recursion_methods import *
def handle_recursion(user, event):
    if event.recursion_type == 'One-Time':
        perform_one_time(user, event)
    elif event.recursion_type == 'daily':
        perform_daily_recursion(user, event)
    elif event.recursion_type == 'weekly':
        perform_weekly_recursion(user, event)
    elif event.recursion_type == 'monthly':
        perform_monthly_recursion(user, event)
    elif event.recursion_type == 'interval':
        perform_interval_recursion(user, event)
    elif event.recursion_type == 'weekday':
        perform_weekday_recursion(user, event)
    elif event.recursion_type == 'relative':
        perform_relative_recursion(user, event)