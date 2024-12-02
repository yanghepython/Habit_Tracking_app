from db import add_habit, increment_habit
from datetime import datetime, timedelta

class Habit:
    def __init__(self, name, frequency, streak=0, last_completed=None, completed = 0): #hasi: completed added here
        """Habit: to track the habit of users"""
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.last_completed = last_completed
        self.completed_tasks = completed
        self.completed_dates = []  # To save the completed dates

    def mark_completed(self, db):
        """Mark the habit as completed and update streak"""
        completed_date = datetime.now().date()  # Record the current date when marking the habit as completed
        self.completed_tasks += 1
        self.completed_dates.append(completed_date)
        self.streak += 1
        self.last_completed = completed_date

        # Save to the database
        increment_habit(db, self.name)


    def __str__(self):
        dates = ", ".join(map(str, self.completed_dates))  # Get date into str
        return f"Habit: {self.name}, Frequency: {self.frequency}, Completed: {self.completed_tasks}, Streak: {self.streak}, Last Completed: {self.last_completed}"#, Dates: [{dates}] #hasi: self.last_completed added here and [{dates}] commented out

    def store(self, db):
        """Store habit in the database"""
        add_habit(db, self.name, self.frequency)

    def add_event(self, db, date: str = None):
        """Add a completed event to the habit"""
        increment_habit(db, self.name, date)

    def reset_streak(self, db):
        """Reset the habit streak in the database and the object"""
        self.streak = 0
        self.last_completed = None
        # Update the database
        cur = db.cursor()
        cur.execute("UPDATE tbl_habit SET streak = ?, last_completed = ? WHERE name = ?", (0, None, self.name))
        db.commit()

    def get_current_streak(self):
        """Returns the current streak from the database"""
        return self.streak

    def get_last_completed(self):
        """Returns the last completed date from the database"""
        return self.last_completed
