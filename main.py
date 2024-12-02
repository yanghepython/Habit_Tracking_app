from db import get_db, get_all_habits, delete_habit
from habit import Habit
from analyse import plot_streaks_as_table


def display_menu():
    print("\nHabit Tracker Menu:")
    print("1. Add Habit")
    print("2. Mark Habit as Completed")
    print("3. View Habits")
    print("4. Analyze Habits (Show Streaks in Table)")
    print("5. Delete a Habit")
    print("6. Exit")




def main():

    db = get_db()

    ls_habits = []
    # Load existing habits from the database
    for habit_data in get_all_habits(db):
        habit_name, frequency, streak, completed, last_completed = habit_data
        ls_habits.append(Habit(habit_name, frequency, streak, last_completed, completed))

    print(f"Loaded habits: {get_all_habits(db)}")

    default_choices = [
        "1. English learning",
        "2. Teeth protection with Elmex gelee",
        "3. Go to the eye doctor",
        "4. Financial review",
        "5. Gym training"
    ]

    while True:
        display_menu()
        choice = input("Select an option (1-7): ")

        if choice == '1':  # Add a Habit
            print("Choose a habit:")
            for option in default_choices:
                print(option)

            selection = input("Enter the number of your choice or type 'new' to enter a new habit: ")
            if selection.lower() == 'new':
                custom_habit = input("Enter the habit name: ")
            else:
                try:
                    selected_index = int(selection) - 1
                    if 0 <= selected_index < len(default_choices):
                        custom_habit = default_choices[selected_index].split(". ")[1]
                    else:
                        print("Invalid selection. Please enter a valid number or type 'new'.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number or type 'new'.")
                    continue
            existing_habits = get_all_habits(db)
            habit_names = [habit[0] for habit in existing_habits]
            if custom_habit in habit_names:
                print(f"Habit '{custom_habit}' already exists! Please choose a different name.")
                continue
            frequency = input("Enter the frequency (daily, weekly, monthly, yearly): ").lower()
            if frequency in ['daily', 'weekly', 'monthly', 'yearly']:
                new_habit = Habit(custom_habit, frequency)
                new_habit.store(db)
                ls_habits.append(new_habit)
                print(f"Habit '{custom_habit}' added with frequency '{frequency}'.")
            else:
                print("Invalid frequency. Please choose from daily, weekly, monthly, or yearly.")

        elif choice == '2':  # Mark a Habit as Completed
            if not ls_habits:
                print("No habits to mark as completed.")
                continue
            print("Select a habit to mark as completed:")
            for index, habit in enumerate(ls_habits):
                print(f"{index + 1}. {habit.name} (Frequency: {habit.frequency})")
            habit_index = int(input("Enter the habit number: ")) - 1
            if 0 <= habit_index < len(ls_habits):
                ls_habits[habit_index].mark_completed(db)


            else:
                print("Invalid habit number.")

        elif choice == '3':  # View Habits
            if not ls_habits:
                print("No habits to display.")
            else:
                for habit in ls_habits:
                    print(habit)
                    if habit.frequency == 'daily' and habit.get_current_streak() >= 21:
                        print("  → You've developed a good habit! Keep it up!")

        elif choice == '4':  # Analyze Habits
            plot_streaks_as_table(db)


        elif choice == '5':  # Delete a Habit

            if not ls_habits:
                print("No habits to delete.")

                continue

            print("Select a habit to delete:")

            for index, habit in enumerate(ls_habits):
                print(f"{index + 1}. {habit.name} (Frequency: {habit.frequency})")

            try:

                habit_index = int(input("Enter the habit number to delete: ")) - 1

                if 0 <= habit_index < len(ls_habits):

                    habit_to_delete = ls_habits.pop(habit_index)

                    # 使用 delete_habit 函数删除数据库中的习惯和跟踪数据

                    delete_habit(db, habit_to_delete.name)

                    print(f"Habit '{habit_to_delete.name}' has been deleted.")

                else:

                    print("Invalid habit number.")

            except ValueError:

                print("Invalid input. Please enter a valid number.")


        elif choice == '6':  # Exit
            print("Exiting the Habit Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
