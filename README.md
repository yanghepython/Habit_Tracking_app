# My Habit Tracking App
This is a Python-based application designed to help users track their habits, monitor their progress, and maintain consistency. The app allows users to add, mark as completed, view, and delete habits, as well as analyze their performance with streak data. This app is backed by an SQLite database to store habit data and completed task records.
## Features
Add a habit: Users can create new habits with customizable frequencies (daily, weekly, monthly, yearly).
Track habit completion: Users can mark a habit as completed each day, which updates their habit streak.
View habit progress: Display a list of all habits, their completion streaks, and frequencies.
Analyze habits: Generate reports on the total streak and longest streak for each habit, visualized in a table.
Delete a habit: Users can remove a habit and its associated completion data from the app.



## Setup
To set up the project, clone the repository and install the required dependencies:
```
pip install -r requirements.txt
```

## Installation
Install the required Python packages in requirements.txt by running:
```
pip install matplotlib
pip install sqlite3
```


## Usage

1. Running the App
To start the Habit Tracker App, run the main.py script:

```
python main.py
```
2. Menu Options
Once the app starts, the user will be presented with the following menu options:

Add Habit: Add a new habit to track.
Mark Habit as Completed: Mark a selected habit as completed for the current day.
View Habits: View a list of all habits with their completion streaks and other details.
Analyze Habits: Show a table displaying the total streak and longest streak for each habit. It also includes some congratulatory messages when certain streak milestones are reached.
Delete a Habit: Delete an existing habit along with its tracked data.
Exit: Exit the application.

3. Example Workflow
Add Habit:
Select an existing habit or enter a new habit.
Define its frequency (daily, weekly, monthly, or yearly).
Mark Habit as Completed:
Select a habit to mark as completed.
The streak is updated accordingly, and the completion is recorded in the database.
View Habits:
View a list of habits along with their current streak and frequency.
Analyze Habits:
The app displays a summary of the habit streaks in both a textual table and a graphical format using matplotlib.
Delete Habit:
Remove a habit, and all its associated completion data is deleted from the database.

Example Output
```
Habit Tracker Menu:
1. Add Habit
2. Mark Habit as Completed
3. View Habits
4. Analyze Habits (Show Streaks in Table)
5. Delete a Habit
6. Exit

Select an option (1-6): 1
Choose a habit:
1. English learning
2. Teeth protection with Elmex gelee
...
Enter the number of your choice or type 'new' to enter a new habit: new
Enter the habit name: Reading
Enter the frequency (daily, weekly, monthly, yearly): daily
Habit 'Reading' added with frequency 'daily'.
```

## Test
Running Tests
To run the tests, make sure pytest is installed and run the following command:
```
pytest test.py
```
pytest will automatically discover and run all the test functions prefixed with test_.

Mock Database for Tests
The tests use a mock SQLite database that is set up for each test using the pytest.fixture decorator. The mock database is populated with test data to simulate the habit tracking system, allowing the tests to run in isolation without modifying any production data.

## Contributing
Feel free to contribute to the project! Open a pull request with your changes and make sure all tests pass.