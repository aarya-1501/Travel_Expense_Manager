
from datetime import date
import math


# --------------------------------------------------
# SAFE NUMBER CONVERSION
# --------------------------------------------------

def safe_float(value, default=0.0):

    try:
        number = float(value)

        if not math.isfinite(number):
            return default

        return number

    except (TypeError, ValueError):
        return default


# --------------------------------------------------
# TRIP EXPENSE PREDICTION
# --------------------------------------------------

def predict_trip_expense(trip, expenses):

    # Get trip dates
    try:
        start_date = date.fromisoformat(
            str(trip["start_date"])
        )

        end_date = date.fromisoformat(
            str(trip["end_date"])
        )

    except (ValueError, TypeError):
        raise ValueError("Invalid trip dates.")

    today = date.today()

    # Validate trip duration
    if end_date < start_date:
        raise ValueError(
            "Trip end date cannot be earlier than start date."
        )

    # Calculate total trip duration
    trip_days = (end_date - start_date).days + 1

    # Calculate total recorded expenses
    total_expenses = sum(
        safe_float(expense["amount"])
        for expense in expenses
        if safe_float(expense["amount"]) > 0
    )

    # Get planned budget safely
    budget = safe_float(trip["budget"])

    # Calculate elapsed and remaining days
    if today < start_date:

        elapsed_days = 0

    elif today > end_date:

        elapsed_days = trip_days

    else:

        elapsed_days = (today - start_date).days + 1

    remaining_days = trip_days - elapsed_days

    # Calculate average daily spending
    if elapsed_days > 0:

        average_daily_expense = (
            total_expenses / elapsed_days
        )

    else:

        average_daily_expense = 0

    # --------------------------------------------------
    # PREDICT FINAL TRIP EXPENSES
    # --------------------------------------------------

    if today < start_date:

        predicted_total = 0

    elif today > end_date:

        predicted_total = total_expenses

    elif total_expenses > 0:

        predicted_total = (
            average_daily_expense * trip_days
        )

    else:

        predicted_total = 0

    # --------------------------------------------------
    # BUDGET COMPARISON
    # --------------------------------------------------

    budget_difference = budget - predicted_total

    if today < start_date:

        budget_status = "Trip Not Started"

    elif today > end_date:

        budget_status = "Trip Completed"

    elif total_expenses == 0:

        budget_status = "Not Enough Expense Data"

    elif predicted_total > budget:

        budget_status = "Budget Overrun Expected"

    else:

        budget_status = "Within Budget"

    # --------------------------------------------------
    # RETURN PREDICTION RESULTS
    # --------------------------------------------------

    return {
        "trip_days": trip_days,
        "elapsed_days": elapsed_days,
        "remaining_days": remaining_days,
        "total_expenses": total_expenses,
        "average_daily_expense": average_daily_expense,
        "predicted_total": predicted_total,
        "budget": budget,
        "budget_difference": budget_difference,
        "budget_status": budget_status
    }
