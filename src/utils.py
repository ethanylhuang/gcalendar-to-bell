from tabulate import tabulate


def print_schedule_events(schedule_events):
    table_data = [
        [date, event.schedule_type, event.display_name]
        for date, event in schedule_events.items()
    ]
    print(tabulate(table_data, headers=["Date", "Type", "Name"], tablefmt="grid"))
