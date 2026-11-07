
import streamlit as st
from supabase import create_client
from pathlib import Path
from collections import defaultdict


# --------------------------------------------------
# SUPABASE CONNECTION
# --------------------------------------------------

@st.cache_resource
def get_connection():

    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

def create_tables():
    # Tables have already been created in Supabase.
    pass


# --------------------------------------------------
# ADD A NEW TRIP
# --------------------------------------------------

def add_trip(trip_name, destination, start_date, end_date, budget, description):

    supabase = get_connection()

    response = supabase.table("trips").insert({
        "trip_name": trip_name,
        "destination": destination,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "budget": float(budget),
        "description": description
    }).execute()

    return response.data[0]["trip_id"]


# --------------------------------------------------
# GET ALL SAVED TRIPS
# --------------------------------------------------

def get_all_trips():

    supabase = get_connection()

    response = (
        supabase.table("trips")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


# --------------------------------------------------
# ADD A NEW EXPENSE
# --------------------------------------------------

def add_expense(trip_id, category, amount, expense_date, description):

    supabase = get_connection()

    response = supabase.table("expenses").insert({
        "trip_id": int(trip_id),
        "category": category,
        "amount": float(amount),
        "expense_date": str(expense_date),
        "description": description
    }).execute()

    return response.data[0]["expense_id"]


# --------------------------------------------------
# GET ALL SAVED EXPENSES
# --------------------------------------------------

def get_all_expenses():

    supabase = get_connection()

    response = (
        supabase.table("expenses")
        .select("*, trips!inner(trip_name, destination)")
        .order("expense_date", desc=True)
        .execute()
    )

    expenses = []

    for row in response.data:

        trip = row.pop("trips")

        row["trip_name"] = trip["trip_name"]
        row["destination"] = trip["destination"]

        expenses.append(row)

    return expenses


# --------------------------------------------------
# UPDATE AN EXISTING EXPENSE
# --------------------------------------------------

def update_expense(expense_id, category, amount, expense_date, description):

    supabase = get_connection()

    supabase.table("expenses").update({
        "category": category,
        "amount": float(amount),
        "expense_date": str(expense_date),
        "description": description
    }).eq("expense_id", int(expense_id)).execute()


# --------------------------------------------------
# DELETE AN EXISTING EXPENSE
# --------------------------------------------------

def delete_expense(expense_id):

    supabase = get_connection()

    supabase.table("expenses").delete().eq(
        "expense_id", int(expense_id)
    ).execute()


# --------------------------------------------------
# GET DASHBOARD SUMMARY
# --------------------------------------------------

def get_dashboard_summary():

    supabase = get_connection()

    trips = (
        supabase.table("trips")
        .select("budget")
        .execute()
    )

    expenses = (
        supabase.table("expenses")
        .select("amount")
        .execute()
    )

    total_trips = len(trips.data)

    total_budget = sum(
        float(row["budget"]) for row in trips.data
    )

    total_expenses = sum(
        float(row["amount"]) for row in expenses.data
    )

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

    supabase = get_connection()

    response = (
        supabase.table("expenses")
        .select("category, amount")
        .execute()
    )

    category_totals = defaultdict(float)

    for row in response.data:

        category_totals[row["category"]] += float(row["amount"])

    result = [
        {
            "category": category,
            "total_amount": amount
        }
        for category, amount in category_totals.items()
    ]

    return sorted(
        result,
        key=lambda x: x["total_amount"],
        reverse=True
    )


# --------------------------------------------------
# GET EXPENSES BY TRIP
# --------------------------------------------------

def get_expenses_by_trip():

    supabase = get_connection()

    trips = (
        supabase.table("trips")
        .select("trip_id, trip_name, destination")
        .execute()
    )

    expenses = (
        supabase.table("expenses")
        .select("trip_id, amount")
        .execute()
    )

    trip_totals = defaultdict(float)

    for expense in expenses.data:

        trip_totals[expense["trip_id"]] += float(
            expense["amount"]
        )

    result = []

    for trip in trips.data:

        result.append({
            "trip_name": trip["trip_name"],
            "destination": trip["destination"],
            "total_amount": trip_totals[trip["trip_id"]]
        })

    return sorted(
        result,
        key=lambda x: x["total_amount"],
        reverse=True
    )


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

    supabase = get_connection()

    response = supabase.table("prediction_history").insert({

        "trip_id": int(trip_id),

        "predicted_total": float(predicted_total),

        "actual_expenses_at_prediction": float(
            actual_expenses_at_prediction
        ),

        "planned_budget": float(planned_budget),

        "elapsed_days": int(elapsed_days),

        "trip_days": int(trip_days)

    }).execute()

    return response.data[0]["prediction_id"]


# --------------------------------------------------
# GET PREDICTION HISTORY FOR A TRIP
# --------------------------------------------------

def get_prediction_history(trip_id):

    supabase = get_connection()

    response = (
        supabase.table("prediction_history")
        .select("*, trips!inner(trip_name, destination)")
        .eq("trip_id", int(trip_id))
        .order("prediction_date", desc=True)
        .order("prediction_id", desc=True)
        .execute()
    )

    history = []

    for row in response.data:

        trip = row.pop("trips")

        row["trip_name"] = trip["trip_name"]
        row["destination"] = trip["destination"]

        history.append(row)

    return history


# --------------------------------------------------
# GET ALL PREDICTION HISTORY
# --------------------------------------------------

def get_all_prediction_history():

    supabase = get_connection()

    response = (
        supabase.table("prediction_history")
        .select("*, trips!inner(trip_name, destination)")
        .order("prediction_date", desc=True)
        .order("prediction_id", desc=True)
        .execute()
    )

    history = []

    for row in response.data:

        trip = row.pop("trips")

        row["trip_name"] = trip["trip_name"]
        row["destination"] = trip["destination"]

        history.append(row)

    return history
