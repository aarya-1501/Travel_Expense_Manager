
import streamlit as st

from database.database import (
    create_tables,
    get_all_trips,
    add_expense,
    get_all_expenses
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Add Expense | Travel Expense Manager",
    page_icon="💰",
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

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden;
}

[data-testid="stMainMenu"] {
    visibility: hidden;
}

[data-testid="stAppDeployButton"] {
    display: none !important;
}

section[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background-color: #faf8ff;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stMain"] {
    padding-top: 0 !important;
}

section.main {
    padding-top: 0 !important;
}

section.main > div {
    padding-top: 0 !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.main-heading {
    color: #55416d;
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    margin-top: 0;
    padding-top: 5px;
}

.sub-heading {
    color: #88769f;
    text-align: center;
    font-size: 16px;
    margin-bottom: 25px;
}

.section-heading {
    color: #55416d;
    font-size: 27px;
    font-weight: 650;
    margin-top: 35px;
    margin-bottom: 8px;
}

.section-description {
    color: #88769f;
    font-size: 14px;
    margin-bottom: 20px;
}

div[data-testid="stForm"] {
    background-color: #ffffff;
    border: 1px solid #e9e0f2;
    border-radius: 15px;
    padding: 25px;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 9px;
    border-color: #e3d9ee;
}

.stDateInput input {
    border-radius: 9px;
    border-color: #e3d9ee;
}

.stButton button,
.stFormSubmitButton button {
    background-color: #8e75ad;
    color: white;
    border: none;
    border-radius: 9px;
    transition: background-color 0.3s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #72578f;
    color: white;
}

[data-testid="stExpander"] {
    background-color: #ffffff;
    border: 1px solid #e9e0f2;
    border-radius: 12px;
    margin-bottom: 12px;
}

[data-testid="stExpander"] summary {
    color: #55416d;
    font-weight: 600;
}

.trip-heading {
    color: #55416d;
    font-size: 21px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    color: #927fa8;
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE HEADING
# --------------------------------------------------

st.markdown(
    '<div class="main-heading">💰 Add Expense</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">'
    'Keep track of your travel spending, one expense at a time.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# ADD NEW EXPENSE
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Add a New Expense</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter your expense details and link them to your trip.'
    '</div>',
    unsafe_allow_html=True
)


# Retrieve Available Trips

trips = get_all_trips()


if not trips:

    st.warning(
        "Please create a trip first before adding expenses."
    )

else:

    trip_options = {
        f"{trip['trip_name']} - {trip['destination']}": trip['trip_id']
        for trip in trips
    }

    # Expense Form

    with st.form("expense_form"):

        selected_trip = st.selectbox(
            "Select Trip",
            options=list(trip_options.keys())
        )

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Transport",
                "Accommodation",
                "Shopping",
                "Entertainment",
                "Other"
            ]
        )

        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        expense_date = st.date_input(
            "Expense Date"
        )

        description = st.text_area(
            "Expense Description",
            placeholder="Describe what this expense was for..."
        )

        submit = st.form_submit_button(
            "💰 Add Expense",
            use_container_width=True
        )

        if submit:

            # VALIDATION 1: Check amount

            if amount <= 0:

                st.error(
                    "Please enter an expense amount greater than ₹0."
                )

            # VALIDATION 2: Check selected trip

            elif selected_trip not in trip_options:

                st.error(
                    "Please select a valid trip."
                )

            else:

                selected_trip_id = trip_options[selected_trip]

                # Find selected trip details

                selected_trip_details = next(
                    (
                        trip for trip in trips
                        if trip["trip_id"] == selected_trip_id
                    ),
                    None
                )

                if selected_trip_details is None:

                    st.error(
                        "Selected trip could not be found."
                    )

                else:

                    # Convert trip dates into date objects

                    from datetime import date

                    start_date = date.fromisoformat(
                        str(selected_trip_details["start_date"])
                    )

                    end_date = date.fromisoformat(
                        str(selected_trip_details["end_date"])
                    )

                    # VALIDATION 3: Check expense date

                    if expense_date < start_date or expense_date > end_date:

                        st.error(
                            f"Expense date must be between "
                            f"{start_date.strftime('%d-%m-%Y')} and "
                            f"{end_date.strftime('%d-%m-%Y')} "
                            f"for this trip."
                        )

                    else:

                        # Save expense only after validation

                        expense_id = add_expense(
                            selected_trip_id,
                            category,
                            amount,
                            expense_date,
                            description.strip()
                        )

                        st.success(
                            f"Expense added successfully! "
                            f"Expense ID: {expense_id}"
                        )

                        st.rerun()


# --------------------------------------------------
# DISPLAY SAVED EXPENSES TRIP-WISE
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">My Saved Expenses</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Your expenses are organized separately for each trip.'
    '</div>',
    unsafe_allow_html=True
)


# Retrieve All Expenses

expenses = get_all_expenses()


if expenses:

    # Group expenses by trip ID

    grouped_expenses = {}

    for expense in expenses:

        trip_id = expense["trip_id"]

        if trip_id not in grouped_expenses:
            grouped_expenses[trip_id] = []

        grouped_expenses[trip_id].append(expense)


    # Display each trip separately

    for trip in trips:

        trip_id = trip["trip_id"]

        trip_expenses = grouped_expenses.get(trip_id, [])

        if trip_expenses:

            total_trip_expense = sum(
                float(expense["amount"])
                for expense in trip_expenses
            )

            st.markdown(
                f'<div class="trip-heading">'
                f'✈️ {trip["trip_name"]} - {trip["destination"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.caption(
                f"Total Expenses: ₹{total_trip_expense:,.2f} "
                f"| Number of Expenses: {len(trip_expenses)}"
            )

            for expense in trip_expenses:

                with st.expander(
                    f"💰 {expense['category']} - "
                    f"₹{expense['amount']:,.2f}"
                ):

                    st.write(
                        f"**Expense ID:** {expense['expense_id']}"
                    )

                    st.write(
                        f"**Trip:** {expense['trip_name']}"
                    )

                    st.write(
                        f"**Destination:** {expense['destination']}"
                    )

                    st.write(
                        f"**Category:** {expense['category']}"
                    )

                    st.write(
                        f"**Amount:** ₹{expense['amount']:,.2f}"
                    )

                    st.write(
                        f"**Date:** {expense['expense_date']}"
                    )

                    st.write(
                        f"**Description:** "
                        f"{expense['description'] or 'No description provided.'}"
                    )

            st.divider()

else:

    st.info(
        "No expenses recorded yet. Add your first expense!"
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
