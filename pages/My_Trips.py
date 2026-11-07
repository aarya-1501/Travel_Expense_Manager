
import streamlit as st
from datetime import date

from database.database import create_tables, add_trip, get_all_trips


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="My Trips | Travel Expense Manager",
    page_icon="✈️",
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
.stNumberInput input {
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
    '<div class="main-heading">✈️ My Trips</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">'
    'Create, organize and manage all your travel plans in one place.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# CREATE NEW TRIP
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Create a New Trip</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Plan your next journey by entering the details below.'
    '</div>',
    unsafe_allow_html=True
)


# Trip Form

with st.form("trip_form"):

    trip_name = st.text_input(
        "Trip Name",
        placeholder="Example: Goa Vacation"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Example: Goa, India"
    )

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date",
            min_value=date.today()
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            min_value=date.today()
        )

    budget = st.number_input(
        "Total Budget (₹)",
        min_value=0.0,
        step=500.0,
        format="%.2f"
    )

    description = st.text_area(
        "Trip Description",
        placeholder="Add a few details about your trip..."
    )

    submit = st.form_submit_button(
        "✈️ Create Trip",
        use_container_width=True
    )


# --------------------------------------------------
# FORM VALIDATION AND DATABASE INSERTION
# --------------------------------------------------

if submit:

    # Clean unnecessary spaces

    trip_name = trip_name.strip()
    destination = destination.strip()
    description = description.strip()

    # VALIDATION 1: Trip name

    if not trip_name:

        st.error("Please enter a valid trip name.")

    # VALIDATION 2: Destination

    elif not destination:

        st.error("Please enter a valid destination.")

    # VALIDATION 3: Start date

    elif start_date < date.today():

        st.error("Trip start date cannot be in the past.")

    # VALIDATION 4: End date

    elif end_date < start_date:

        st.error("End date cannot be before the start date.")

    # VALIDATION 5: Budget

    elif budget <= 0:

        st.error("Please enter a trip budget greater than ₹0.")

    else:

        # Save trip only after validation

        trip_id = add_trip(
            trip_name,
            destination,
            start_date,
            end_date,
            budget,
            description
        )

        st.success(
            f"Trip created successfully! Your Trip ID is {trip_id}."
        )

        st.rerun()


# --------------------------------------------------
# DISPLAY SAVED TRIPS
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">My Saved Trips</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'All your planned journeys, together in one place.'
    '</div>',
    unsafe_allow_html=True
)


trips = get_all_trips()


if trips:

    for trip in trips:

        with st.expander(
            f"✈️ {trip['trip_name']} - {trip['destination']}"
        ):

            st.write(f"**Trip ID:** {trip['trip_id']}")

            st.write(f"**Destination:** {trip['destination']}")

            st.write(f"**Start Date:** {trip['start_date']}")

            st.write(f"**End Date:** {trip['end_date']}")

            st.write(f"**Budget:** ₹{trip['budget']:,.2f}")

            st.write(
                f"**Description:** "
                f"{trip['description'] or 'No description provided.'}"
            )

else:

    st.info("No trips found. Create your first trip!")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Made with 💜 for every journey.<br>
    Travel Expense Manager
</div>
""", unsafe_allow_html=True)
