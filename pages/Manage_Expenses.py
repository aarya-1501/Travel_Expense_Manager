
import streamlit as st

from database.database import (
    create_tables,
    get_all_trips,
    get_all_expenses,
    update_expense,
    delete_expense
)

from datetime import date


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Manage Expenses | Travel Expense Manager",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_tables()

if "editing_expense_id" not in st.session_state:
    st.session_state.editing_expense_id = None

if "confirm_delete_expense_id" not in st.session_state:
    st.session_state.confirm_delete_expense_id = None


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
    padding-top: 5px !important;
    max-width: 1250px !important;
}

.stApp {
    background-color: #faf8ff;
}

.main-heading {
    text-align: center;
    font-size: 38px;
    font-weight: 750;
    color: #55416d;
    padding-top: 5px;
    margin-bottom: 5px;
}

.sub-heading {
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

.trip-heading {
    color: #55416d;
    font-size: 23px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 5px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #e9e0f2 !important;
    border-radius: 12px !important;
}

[data-testid="stForm"] {
    background-color: #ffffff !important;
    border: 1px solid #e9e0f2 !important;
    border-radius: 15px !important;
    padding: 25px !important;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px !important;
}

.stButton > button,
.stFormSubmitButton > button {
    background-color: #8e75ad !important;
    color: white !important;
    border: 1px solid #8e75ad !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
    padding: 9px 15px !important;
    transition: 0.2s ease !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #72578f !important;
    border-color: #72578f !important;
    color: white !important;
}

hr {
    border-color: #e9e0f2 !important;
}

.footer {
    text-align: center;
    color: #88769f;
    font-size: 13px;
    padding: 25px 0 15px 0;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE HEADING
# --------------------------------------------------

st.markdown(
    '<div class="main-heading">📝 Manage Expenses</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">'
    'View, edit and manage your travel expenses trip by trip.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# RETRIEVE TRIPS AND EXPENSES
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">My Trips & Expenses</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Search and filter your expenses, or use the Edit and Delete '
    'buttons to manage individual records.'
    '</div>',
    unsafe_allow_html=True
)

trips = get_all_trips()
expenses = get_all_expenses()


# --------------------------------------------------
# EXPENSE SEARCH AND FILTERS
# --------------------------------------------------

st.markdown("### 🔎 Search & Filter Expenses")

filtered_expenses = []

search_trip = ""
selected_category = "All Categories"

if expenses:

    categories = sorted(set(
        expense["category"]
        for expense in expenses
        if expense["category"]
    ))

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        search_trip = st.text_input(
            "🔍 Search by Trip Name or Destination",
            placeholder="Example: Goa, Singapore..."
        )

    with filter_col2:

        selected_category = st.selectbox(
            "📂 Filter by Expense Category",
            ["All Categories"] + categories
        )

    st.divider()

    trip_lookup = {
        trip["trip_id"]: trip
        for trip in trips
    }

    for expense in expenses:

        expense_trip = trip_lookup.get(
            expense["trip_id"]
        )

        if expense_trip is None:
            continue

        trip_text = (
            str(expense_trip["trip_name"]) + " " +
            str(expense_trip["destination"])
        ).lower()

        if search_trip.strip():

            if search_trip.strip().lower() not in trip_text:
                continue

        if selected_category != "All Categories":

            if expense["category"] != selected_category:
                continue

        filtered_expenses.append(expense)


    # --------------------------------------------------
    # FILTERED EXPENSE SUMMARY
    # --------------------------------------------------

    filtered_total = sum(
        float(expense["amount"])
        for expense in filtered_expenses
    )

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.metric(
            "💰 Total Filtered Expenses",
            f"₹{filtered_total:,.2f}"
        )

    with summary_col2:

        st.metric(
            "🧾 Number of Expenses",
            len(filtered_expenses)
        )

else:

    st.info(
        "No expenses available to search or filter yet."
    )


# --------------------------------------------------
# GROUP FILTERED EXPENSES BY TRIP
# --------------------------------------------------

if trips:

    grouped_expenses = {}

    for expense in filtered_expenses:

        trip_id = expense["trip_id"]

        if trip_id not in grouped_expenses:
            grouped_expenses[trip_id] = []

        grouped_expenses[trip_id].append(expense)


    # --------------------------------------------------
    # DISPLAY FILTERED TRIPS
    # --------------------------------------------------

    st.markdown("### ✈️ Filtered Trip Expenses")

    displayed_trips = 0

    for trip in trips:

        trip_id = trip["trip_id"]

        trip_expenses = grouped_expenses.get(
            trip_id, []
        )

        if not trip_expenses:
            continue

        displayed_trips += 1

        st.markdown(
            f'<div class="trip-heading">'
            f'✈️ {trip["trip_name"]} - {trip["destination"]}'
            f'</div>',
            unsafe_allow_html=True
        )

        total_expense = sum(
            float(expense["amount"])
            for expense in trip_expenses
        )

        st.caption(
            f"Total Expenses: ₹{total_expense:,.2f} "
            f"| Number of Expenses: {len(trip_expenses)}"
        )


        # --------------------------------------------------
        # DISPLAY INDIVIDUAL EXPENSES
        # --------------------------------------------------

        for expense in trip_expenses:

            expense_id = expense["expense_id"]

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [5, 1.2, 1.2],
                    vertical_alignment="center"
                )

                with col1:

                    st.markdown(
                        f"**💰 {expense['category']}**"
                    )

                    st.write(
                        f"₹{expense['amount']:,.2f} "
                        f"• {expense['expense_date']}"
                    )

                    st.caption(
                        expense["description"]
                        or "No description provided."
                    )

                with col2:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{expense_id}",
                        use_container_width=True
                    ):

                        st.session_state.editing_expense_id = expense_id
                        st.rerun()

                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{expense_id}",
                        use_container_width=True
                    ):

                        st.session_state.confirm_delete_expense_id = expense_id
                        st.rerun()


                # --------------------------------------------------
                # DELETE CONFIRMATION
                # --------------------------------------------------

                if st.session_state.confirm_delete_expense_id == expense_id:

                    st.warning(
                        "Are you sure you want to delete this expense? "
                        "This action cannot be undone."
                    )

                    confirm_col1, confirm_col2 = st.columns(2)

                    with confirm_col1:

                        if st.button(
                            "Yes, Delete",
                            key=f"confirm_delete_{expense_id}",
                            use_container_width=True
                        ):

                            delete_expense(expense_id)

                            st.session_state.confirm_delete_expense_id = None

                            if st.session_state.editing_expense_id == expense_id:
                                st.session_state.editing_expense_id = None

                            st.rerun()

                    with confirm_col2:

                        if st.button(
                            "Cancel",
                            key=f"cancel_delete_{expense_id}",
                            use_container_width=True
                        ):

                            st.session_state.confirm_delete_expense_id = None
                            st.rerun()


                # --------------------------------------------------
                # EDIT FORM
                # --------------------------------------------------

                if st.session_state.editing_expense_id == expense_id:

                    st.divider()

                    st.markdown(
                        "### ✏️ Edit Expense Details"
                    )

                    edit_categories = [
                        "Food",
                        "Transport",
                        "Accommodation",
                        "Shopping",
                        "Entertainment",
                        "Other"
                    ]

                    current_category = expense["category"]

                    if current_category not in edit_categories:
                        edit_categories.append(current_category)

                    category_index = edit_categories.index(
                        current_category
                    )

                    original_expense_date = date.fromisoformat(
                        str(expense["expense_date"])
                    )

                    with st.form(
                        f"edit_form_{expense_id}"
                    ):

                        updated_category = st.selectbox(
                            "Expense Category",
                            edit_categories,
                            index=category_index
                        )

                        updated_amount = st.number_input(
                            "Expense Amount (₹)",
                            min_value=0.0,
                            value=float(expense["amount"]),
                            step=100.0,
                            format="%.2f"
                        )

                        updated_date = st.date_input(
                            "Expense Date",
                            value=original_expense_date
                        )

                        updated_description = st.text_area(
                            "Description",
                            value=expense["description"] or ""
                        )

                        update_button = st.form_submit_button(
                            "💜 Save Changes",
                            use_container_width=True
                        )

                        if update_button:

                            # VALIDATION 1: Amount

                            if updated_amount <= 0:

                                st.error(
                                    "Please enter an expense amount greater than ₹0."
                                )

                            # VALIDATION 2: Category

                            elif not updated_category.strip():

                                st.error(
                                    "Please select a valid expense category."
                                )

                            else:

                                # Find the trip associated with this expense

                                selected_trip = next(
                                    (
                                        trip for trip in trips
                                        if trip["trip_id"] == expense["trip_id"]
                                    ),
                                    None
                                )

                                if selected_trip is None:

                                    st.error(
                                        "The associated trip could not be found."
                                    )

                                else:

                                    trip_start = date.fromisoformat(
                                        str(selected_trip["start_date"])
                                    )

                                    trip_end = date.fromisoformat(
                                        str(selected_trip["end_date"])
                                    )

                                    # VALIDATION 3: Expense date

                                    if not (
                                        trip_start <= updated_date <= trip_end
                                    ):

                                        st.error(
                                            f"Expense date must be between "
                                            f"{trip_start.strftime('%d-%m-%Y')} "
                                            f"and {trip_end.strftime('%d-%m-%Y')}."
                                        )

                                    else:

                                        # Save validated changes

                                        update_expense(
                                            expense_id,
                                            updated_category,
                                            updated_amount,
                                            updated_date,
                                            updated_description.strip()
                                        )

                                        st.session_state.editing_expense_id = None

                                        st.success(
                                            "Expense updated successfully!"
                                        )

                                        st.rerun()


                    if st.button(
                        "Cancel Editing",
                        key=f"cancel_{expense_id}"
                    ):

                        st.session_state.editing_expense_id = None
                        st.rerun()

        st.divider()


    # --------------------------------------------------
    # NO MATCHING EXPENSES
    # --------------------------------------------------

    if displayed_trips == 0:

        st.warning(
            "No expenses match your selected search and filters. "
            "Try changing your search or category."
        )

else:

    st.info(
        "No trips available. Create a trip first to manage its expenses."
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
