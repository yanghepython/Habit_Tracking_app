import sqlite3
from datetime import datetime

def get_db(db_name="habits.db"):
    """
    Connect to the SQLite database. By default, it creates a database file called "habits.db".
    """
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Use Row to access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # 确保外键约束开启
    create_tables(conn)  # Ensure tables are created
    return conn

def create_tables(db):
    """
    Create the necessary tables for the habit tracker.
    """
    cur = db.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tbl_habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        frequency TEXT NOT NULL,
        streak INTEGER DEFAULT 0,
        last_completed DATE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tbl_tracker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habitname TEXT NOT NULL,
        completed_date DATE NOT NULL,
        FOREIGN KEY (habitname) REFERENCES tbl_habit (name) ON DELETE CASCADE
    )
    """) # could also just delete from tbl_tracker first to not have a problem with the foreign key constraint
    db.commit()


def add_habit(db, name, frequency):
    """
    Add a new habit to the database.
    """
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO tbl_habit (name, frequency) VALUES (?, ?)", (name, frequency))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(f"Habit '{name}' already exists in the database.")
        raise e

def increment_habit(db, name):
    cur = db.cursor()
    today = datetime.now().date()


    cur.execute("SELECT COUNT(*) FROM tbl_tracker WHERE habitname = ? AND completed_date = ?", (name, today))
    count = cur.fetchone()[0]

    if count > 0:
        print(f"Habit '{name}' has already been marked as completed today ({today}).")
        return  # Avoid duplicates

    try:

        completed_time = datetime.now()
        cur.execute("INSERT INTO tbl_tracker (habitname, completed_date) VALUES (?, ?)", (name, today))

        # update streak
        cur.execute("SELECT streak FROM tbl_habit WHERE name = ?", (name,))
        habit = cur.fetchone()
        if habit:
            new_streak = habit[0] + 1
            cur.execute("UPDATE tbl_habit SET streak = ? WHERE name = ?", (new_streak, name))
        else:

            cur.execute("INSERT INTO tbl_habit (name, streak) VALUES (?, ?)", (name, 1))
            print(f"Habit '{name}' added to the habit table with a streak of 1.")


        db.commit()
        print(f"Habit '{name}' marked as completed on {today}.")
    except Exception as e:
        db.rollback()
        print(f"Error updating habit '{name}': {e}")


def get_habit_tracking_data(db, name):
    """
    Get all completion dates for a given habit.
    """
    cur = db.cursor()
    cur.execute("SELECT completed_date FROM tbl_tracker WHERE habitname = ? ORDER BY completed_date", (name,))
    return cur.fetchall()

def get_all_habits(db):
    """
    Get all habits from the database.
    """
    cur = db.cursor()
    cur.execute("SELECT h.name, h.frequency, h.streak, COALESCE(COUNT(DISTINCT t.completed_date),0) AS completed, MAX(COALESCE(t.completed_date,0)) AS last_completed FROM tbl_habit h LEFT JOIN tbl_tracker t ON h.name = t.habitname GROUP BY h.name, h.frequency, h.streak") #hasi: h.streak, last_completed and completed added to the SELECT clause, LEFT JOIN tbl_tracker added in the FROM clause, GROUP BY clause added (required when using aggregate function like MAX)
    return cur.fetchall()

def delete_habit(db, name):
    """
    Delete a habit and its associated tracker data from the database.
    """
    cur = db.cursor()
    cur.execute("DELETE FROM tbl_tracker WHERE habitname = ?", (name,))
    cur.execute("DELETE FROM tbl_habit WHERE name = ?", (name,))

    db.commit()



