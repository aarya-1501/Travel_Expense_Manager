
import sqlite3
from pathlib import Path

# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DB_PATH = BASE_DIR / "database" / "travel_expenses.db"


# --------------------------------------------------
# CREATE DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------------------------
# CREATE DATABASE TABLES
# --------------------------------------------------

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Create Trips Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (

            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,

            trip_name TEXT NOT NULL,

            destination TEXT NOT NULL,

            start_date TEXT NOT NULL,

            end_date TEXT NOT NULL,

            budget REAL NOT NULL,

            description TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # Create Expenses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (

            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,

            trip_id INTEGER NOT NULL,

            category TEXT NOT NULL,

            amount REAL NOT NULL,

            expense_date TEXT NOT NULL,

            description TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)

        )
    """)

    # Create Prediction History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (

            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,

            trip_id INTEGER NOT NULL,

            prediction_date TEXT DEFAULT CURRENT_TIMESTAMP,

            predicted_total REAL NOT NULL,

            actual_expenses_at_prediction REAL NOT NULL,

            planned_budget REAL NOT NULL,

            elapsed_days INTEGER NOT NULL,

            trip_days INTEGER NOT NULL,

            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)

        )
    """)

    connection.commit()

    connection.close()


# --------------------------------------------------
# ADD A NEW TRIP
# --------------------------------------------------

def add_trip(trip_name, destination, start_date, end_date, budget, description):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO trips (
            trip_name,
            destination,
            start_date,
            end_date,
            budget,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        trip_name,
        destination,
        str(start_date),
        str(end_date),
        budget,
        description
    ))

    connection.commit()

    trip_id = cursor.lastrowid

    connection.close()

    return trip_id


# --------------------------------------------------
# GET ALL SAVED TRIPS
# --------------------------------------------------

def get_all_trips():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM trips
        ORDER BY created_at DESC
    """)

    trips = cursor.fetchall()

    connection.close()

    return trips


# --------------------------------------------------
# ADD A NEW EXPENSE
# --------------------------------------------------

def add_expense(trip_id, category, amount, expense_date, description):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            trip_id,
            category,
            amount,
            expense_date,
            description
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        trip_id,
        category,
        amount,
        str(expense_date),
        description
    ))

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return expense_id


# --------------------------------------------------
# GET ALL SAVED EXPENSES
# --------------------------------------------------

def get_all_expenses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            expenses.*,
            trips.trip_name,
            trips.destination
        FROM expenses
        INNER JOIN trips
        ON expenses.trip_id = trips.trip_id
        ORDER BY expenses.expense_date DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# --------------------------------------------------
# UPDATE AN EXISTING EXPENSE
# --------------------------------------------------

def update_expense(expense_id, category, amount, expense_date, description):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            category = ?,
            amount = ?,
            expense_date = ?,
            description = ?
        WHERE expense_id = ?
    """, (
        category,
        amount,
        str(expense_date),
        description,
        expense_id
    ))

    connection.commit()

    connection.close()


# --------------------------------------------------
# DELETE AN EXISTING EXPENSE
# --------------------------------------------------

def delete_expense(expense_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE expense_id = ?
    """, (expense_id,))

    connection.commit()

    connection.close()


# --------------------------------------------------
# GET DASHBOARD SUMMARY
# --------------------------------------------------

def get_dashboard_summary():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_trips,
            COALESCE(SUM(budget), 0) AS total_budget
        FROM trips
    """)

    trip_summary = cursor.fetchone()

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount), 0) AS total_expenses
        FROM expenses
    """)

    expense_summary = cursor.fetchone()

    connection.close()

    total_trips = trip_summary["total_trips"]

    total_budget = trip_summary["total_budget"]

    total_expenses = expense_summary["total_expenses"]

    remaining_balance = total_budget - total_expenses

    return {
        "total_trips": total_trips,
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance
    }


# --------------------------------------------------
# GET EXPENSES BY CATEGORY
# --------------------------------------------------

def get_expenses_by_category():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total_amount
        FROM expenses
        GROUP BY category
        ORDER BY total_amount DESC
    """)

    category_expenses = cursor.fetchall()

    connection.close()

    return category_expenses


# --------------------------------------------------
# GET EXPENSES BY TRIP
# --------------------------------------------------

def get_expenses_by_trip():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            trips.trip_name,
            trips.destination,
            COALESCE(SUM(expenses.amount), 0) AS total_amount
        FROM trips
        LEFT JOIN expenses
        ON trips.trip_id = expenses.trip_id
        GROUP BY trips.trip_id
        ORDER BY total_amount DESC
    """)

    trip_expenses = cursor.fetchall()

    connection.close()

    return trip_expenses


# --------------------------------------------------
# SAVE A BUDGET PREDICTION
# --------------------------------------------------

def save_prediction_history(
    trip_id,
    predicted_total,
    actual_expenses_at_prediction,
    planned_budget,
    elapsed_days,
    trip_days
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prediction_history (
            trip_id,
            predicted_total,
            actual_expenses_at_prediction,
            planned_budget,
            elapsed_days,
            trip_days
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        trip_id,
        predicted_total,
        actual_expenses_at_prediction,
        planned_budget,
        elapsed_days,
        trip_days
    ))

    connection.commit()

    prediction_id = cursor.lastrowid

    connection.close()

    return prediction_id


# --------------------------------------------------
# GET PREDICTION HISTORY FOR A TRIP
# --------------------------------------------------

def get_prediction_history(trip_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            prediction_history.*,
            trips.trip_name,
            trips.destination
        FROM prediction_history
        INNER JOIN trips
        ON prediction_history.trip_id = trips.trip_id
        WHERE prediction_history.trip_id = ?
        ORDER BY prediction_history.prediction_date DESC,
                 prediction_history.prediction_id DESC
    """, (trip_id,))

    history = cursor.fetchall()

    connection.close()

    return history


# --------------------------------------------------
# GET ALL PREDICTION HISTORY
# --------------------------------------------------

def get_all_prediction_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            prediction_history.*,
            trips.trip_name,
            trips.destination
        FROM prediction_history
        INNER JOIN trips
        ON prediction_history.trip_id = trips.trip_id
        ORDER BY prediction_history.prediction_date DESC,
                 prediction_history.prediction_id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history


# --------------------------------------------------
# RUN DATABASE CREATION
# --------------------------------------------------

if __name__ == "__main__":

    create_tables()

    print("Database and tables created successfully!")
    print("Prediction history table is ready!")
