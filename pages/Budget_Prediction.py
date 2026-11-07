
import streamlit as st
import sys
from pathlib import Path
from datetime import date
import pandas as pd

# Add main project folder to Python import path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.database import (
    create_tables,
    get_all_trips,
    get_all_expenses,
    save_prediction_history,
    get_prediction_history
)

from prediction import predict_trip_expense


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Budget Prediction | Travel Expense Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

header[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"],
#MainMenu,
[data-testid="stMainMenu"],
[data-testid="stAppDeployButton"] {
    display: none !important;
}

section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 5px !important;
    padding-bottom: 0px !important;
}

.stApp {
    background-color: #faf8ff;
}

.main-heading {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #55416d;
    padding-top: 5px;
}

.main-subtitle {
    text-align: center;
    font-size: 16px;
    color: #88769f;
    margin-bottom: 25px;
}

.section-heading {
    font-size: 27px;
    font-weight: 650;
    color: #55416d;
    margin-top: 35px;
    margin-bottom: 8px;
}

.section-description {
    font-size: 14px;
    color: #88769f;
    margin-bottom: 20px;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e9e0f2;
    border-radius: 13px;
    padding: 18px;
}

.stButton > button {
    background-color: #8e75ad !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #72578f !important;
}

div[data-baseweb="select"] > div {
    background-color: white;
    border-color: #e9e0f2;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #88769f;
    font-size: 13px;
    padding: 30px 0px 15px 0px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE HEADING
# --------------------------------------------------

st.markdown(
    '<div class="main-heading">📊 Budget Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Estimate your travel expenses and stay within your budget.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FETCH TRIPS AND EXPENSES
# --------------------------------------------------

trips = get_all_trips()
expenses = get_all_expenses()


# --------------------------------------------------
# TRIP SELECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Select Your Trip</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Choose a saved trip to view its spending and budget prediction.'
    '</div>',
    unsafe_allow_html=True
)


if not trips:

    st.warning(
        "No trips found. Please create a trip first in the My Trips page."
    )

else:

    # Create unique labels even if trip names are repeated.
    trip_options = {}

    for trip in trips:

        trip_label = (
            f'{trip["trip_name"]} - '
            f'{trip["destination"]} '
            f'(Trip ID: {trip["trip_id"]})'
        )

        trip_options[trip_label] = trip

    selected_trip_name = st.selectbox(
        "Choose a trip",
        options=list(trip_options.keys())
    )

    selected_trip = trip_options[selected_trip_name]

    selected_trip_id = selected_trip["trip_id"]

    # Get expenses belonging only to selected trip.
    trip_expenses = [
        expense
        for expense in expenses
        if expense["trip_id"] == selected_trip_id
    ]

    # --------------------------------------------------
    # CALCULATE PREDICTION
    # --------------------------------------------------

    try:

        prediction = predict_trip_expense(
            selected_trip,
            trip_expenses
        )

    except (ValueError, KeyError, TypeError) as error:

        st.error(
            f"Unable to calculate prediction: {error}"
        )

        prediction = None

    if prediction is not None:

        # --------------------------------------------------
        # TRIP OVERVIEW
        # --------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-heading">Trip Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Destination",
                selected_trip["destination"]
            )

        with col2:

            st.metric(
                "Planned Budget",
                f'₹{prediction["budget"]:,.2f}'
            )

        with col3:

            st.metric(
                "Recorded Expenses",
                len(trip_expenses)
            )

        # --------------------------------------------------
        # TRIP DURATION ANALYSIS
        # --------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-heading">📅 Trip Duration Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Trip Days",
                f'{prediction["trip_days"]} Days'
            )

        with col2:

            st.metric(
                "Elapsed Days",
                f'{prediction["elapsed_days"]} Days'
            )

        with col3:

            st.metric(
                "Remaining Days",
                f'{prediction["remaining_days"]} Days'
            )

        # --------------------------------------------------
        # EXPENSE ANALYSIS
        # --------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-heading">Expense Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Amount Spent",
                f'₹{prediction["total_expenses"]:,.2f}'
            )

        with col2:

            st.metric(
                "Average Daily Spending",
                f'₹{prediction["average_daily_expense"]:,.2f}'
            )

        # --------------------------------------------------
        # BUDGET PREDICTION RESULTS
        # --------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-heading">🔮 Budget Prediction Results</div>',
            unsafe_allow_html=True
        )

        status = prediction["budget_status"]

        if status == "Trip Not Started":

            st.info(
                "Your trip has not started yet. "
                "Add expenses after your journey begins "
                "to generate a prediction."
            )

        elif status == "Not Enough Expense Data":

            st.info(
                "No expenses have been recorded for this trip yet. "
                "Add some expenses to generate a prediction."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Predicted Total Expense",
                    f'₹{prediction["predicted_total"]:,.2f}'
                )

            with col2:

                if prediction["budget_difference"] >= 0:

                    st.metric(
                        "Budget Remaining",
                        f'₹{prediction["budget_difference"]:,.2f}',
                        delta="Remaining"
                    )

                else:

                    st.metric(
                        "Budget Overrun",
                        f'₹{abs(prediction["budget_difference"]):,.2f}',
                        delta="Over Budget",
                        delta_color="inverse"
                    )

            # --------------------------------------------------
            # BUDGET STATUS
            # --------------------------------------------------

            if status == "Within Budget":

                st.success(
                    "✅ Your predicted expenses are within your planned budget!"
                )

            elif status == "Budget Overrun Expected":

                st.error(
                    "⚠️ Your predicted expenses may exceed your planned budget."
                )

            elif status == "Trip Completed":

                st.success(
                    "Your trip is completed. The displayed amount "
                    "represents your actual recorded expenses."
                )

            # --------------------------------------------------
            # BUDGET UTILIZATION
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">Budget Utilization</div>',
                unsafe_allow_html=True
            )

            budget = prediction["budget"]

            if budget > 0:

                actual_percentage = (
                    prediction["total_expenses"] / budget
                ) * 100

                predicted_percentage = (
                    prediction["predicted_total"] / budget
                ) * 100

                st.write(
                    f"Actual Budget Utilization: "
                    f"{actual_percentage:.2f}%"
                )

                st.progress(
                    min(max(actual_percentage / 100, 0.0), 1.0)
                )

                st.write(
                    f"Predicted Budget Utilization: "
                    f"{predicted_percentage:.2f}%"
                )

                st.progress(
                    min(max(predicted_percentage / 100, 0.0), 1.0)
                )

            else:

                st.warning(
                    "Budget utilization cannot be calculated "
                    "because the planned budget is zero."
                )

            # --------------------------------------------------
            # BUDGET RECOMMENDATION
            # --------------------------------------------------

            st.divider()

            st.markdown(
                '<div class="section-heading">💡 Budget Recommendation</div>',
                unsafe_allow_html=True
            )

            if budget <= 0:

                st.warning(
                    "Your planned budget is zero or invalid. "
                    "Update your trip budget to receive useful "
                    "budget recommendations."
                )

            elif prediction["budget_difference"] > 0:

                st.info(
                    f'Your predicted spending is ₹'
                    f'{prediction["budget_difference"]:,.2f} '
                    f'below your planned budget.'
                )

            elif prediction["budget_difference"] < 0:

                st.warning(
                    f'Your predicted spending exceeds your planned '
                    f'budget by ₹'
                    f'{abs(prediction["budget_difference"]):,.2f}. '
                    f'Consider reducing your spending.'
                )

            else:

                st.info(
                    "Your predicted expenses are exactly equal to your budget."
                )

            # --------------------------------------------------
            # SAVE PREDICTION
            # --------------------------------------------------

            if (
                status in [
                    "Within Budget",
                    "Budget Overrun Expected",
                    "Trip Completed"
                ]
                and prediction["total_expenses"] > 0
            ):

                st.divider()

                st.markdown(
                    '<div class="section-heading">💾 Save Prediction</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    "Save this prediction to compare it with your "
                    "actual expenses later."
                )

                if st.button(
                    "💾 Save Current Prediction",
                    key="save_prediction",
                    use_container_width=True
                ):

                    try:

                        save_prediction_history(
                            trip_id=selected_trip_id,
                            predicted_total=prediction["predicted_total"],
                            actual_expenses_at_prediction=prediction["total_expenses"],
                            planned_budget=prediction["budget"],
                            elapsed_days=prediction["elapsed_days"],
                            trip_days=prediction["trip_days"]
                        )

                        st.success(
                            "Your prediction has been saved successfully!"
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to save prediction: {error}"
                        )

            # --------------------------------------------------
            # PREDICTION HISTORY
            # --------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-heading">📚 Prediction History</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'View previously saved predictions for this trip.'
            '</div>',
            unsafe_allow_html=True
        )

        history = get_prediction_history(selected_trip_id)

        if not history:

            st.info(
                "No prediction history available yet. "
                "Save your first prediction to see it here."
            )

        else:

            trip_end_date = date.fromisoformat(
                str(selected_trip["end_date"])
            )

            trip_completed = date.today() > trip_end_date

            history_data = []

            for record in history:

                row = {
                    "Saved On": record["prediction_date"],
                    "Elapsed Days": record["elapsed_days"],
                    "Predicted Expense": round(
                        float(record["predicted_total"]), 2
                    ),
                    "Actual Spent at Prediction": round(
                        float(record["actual_expenses_at_prediction"]),
                        2
                    )
                }

                # Show comparison only after trip completion.
                if trip_completed:

                    actual_total = prediction["total_expenses"]

                    error = abs(
                        float(record["predicted_total"]) - actual_total
                    )

                    if actual_total > 0:

                        accuracy = max(
                            0,
                            100 - (error / actual_total * 100)
                        )

                        row["Final Actual Expense"] = round(
                            actual_total, 2
                        )

                        row["Prediction Accuracy"] = (
                            f"{accuracy:.2f}%"
                        )

                    else:

                        row["Final Actual Expense"] = 0

                        row["Prediction Accuracy"] = "N/A"

                history_data.append(row)

            st.dataframe(
                pd.DataFrame(history_data),
                use_container_width=True,
                hide_index=True
            )

            if trip_completed:

                st.caption(
                    "Prediction accuracy compares each saved prediction "
                    "against the currently recorded expenses of the "
                    "completed trip. Make sure all expenses have been entered."
                )

            else:

                st.info(
                    "Prediction accuracy will be available after the trip ends."
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Made with 💜 for every journey.<br>
    Travel Expense Manager
</div>
""", unsafe_allow_html=True)
