import matplotlib.pyplot as plt
from db import get_all_habits, get_habit_tracking_data
from datetime import datetime, timedelta

def plot_streaks_as_table(db):
    """Display a table showing total and longest streaks for each habit."""
    habits = get_all_habits(db)  # get all habits
    streak_summary = []  # store statistics for each habit
    congratulations = []


    for habit in habits:
        habit_name = habit[0]
        frequency = habit[1]
        data = get_habit_tracking_data(db, habit_name)


        if not data:
            print(f"No completion data for habit: {habit_name}")
            streak_summary.append([habit_name, 0, 0])  # if no data,0
            continue

        # Get all completion dates and sort them by date
        completed_dates = sorted([datetime.strptime(date[0], "%Y-%m-%d").date() for date in data])

        # calculate streak for the habit
        streaks = []
        current_streak = 0
        last_date = None

        for completed_date in completed_dates:
            if last_date is None or completed_date == last_date + timedelta(days=1):
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1  # 重置 streak

            last_date = completed_date

        # add the last streak
        streaks.append(current_streak)

        # calculate total streak and longest streak
        total_streak = sum(streaks)
        longest_streak = max(streaks)

        # 21 days motivation
        streak_summary.append([habit_name, total_streak, longest_streak])
        if frequency == "daily" and longest_streak >= 21:
            congratulations.append(f"Congratulations! You've developed a daily habit '{habit_name}', keep going!")
        elif frequency == "weekly" and longest_streak >= 4:
            congratulations.append(f"Congratulations! You've developed a weekly habit '{habit_name}', keep going!")
        elif frequency == "monthly" and longest_streak >= 3:
            congratulations.append(f"Congratulations! You've developed a monthly habit '{habit_name}', keep going!")
        elif frequency == "yearly" and longest_streak >= 1:
            congratulations.append(f"Congratulations! You've developed a yearly habit '{habit_name}', keep going!")
        else:
            congratulations.append("")



    if not streak_summary:
        print("No streak data to display.")
        return

    # print congratulations information
    print(f"{'Habit':<20} {'Total Streak (Days)':<20} {'Longest Streak (Days)':<20}")
    print("=" * 60)
    for i, (habit_name, total_streak, longest_streak) in enumerate(streak_summary):
        print(f"{habit_name:<20} {total_streak:<20} {longest_streak:<20}")
        if congratulations[i]:
            print(f"  → {congratulations[i]}")

    #  Matplotlib
    fig, ax = plt.subplots(figsize=(8, len(streak_summary) * 0.5))
    ax.axis("tight")
    ax.axis("off")

    # table content
    table_data = [["Habit", "Total Streak (Days)", "Longest Streak (Days)"]]
    table_data.extend(streak_summary)

    table = ax.table(cellText=table_data, colLabels=None, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_data[0]))))

    plt.title("Habit Streak Summary", pad=10)
    plt.show()

