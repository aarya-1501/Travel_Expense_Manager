
import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Travel Expense Manager",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Hide Streamlit top menu and Deploy button */

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


/* Hide left sidebar */

section[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}


/* Remove top spacing */

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


/* Main heading */

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


/* Section headings */

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


/* Quick Access Cards */

.st-key-my_trips_card,
.st-key-add_expense_card,
.st-key-reports_card,
.st-key-budget_prediction_card {

    background-color: #ffffff !important;
    border: 1px solid #e9e0f2 !important;
    border-radius: 15px !important;
    padding: 15px !important;

    transition: transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
}

.st-key-my_trips_card:hover,
.st-key-add_expense_card:hover,
.st-key-reports_card:hover,
.st-key-budget_prediction_card:hover {

    transform: translateY(-7px);
    border-color: #a58bc3 !important;
    box-shadow: 0 10px 25px rgba(142, 117, 173, 0.22);
}


/* Travel inspiration image sizing */

[data-testid="stImage"] img {
    height: 220px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 12px;
}


/* Inspiration titles */

.inspiration-title {
    color: #55416d;
    font-size: 17px;
    font-weight: 650;
    margin-top: 9px;
    margin-bottom: 3px;
}

.inspiration-caption {
    color: #88769f;
    font-size: 13px;
    margin-bottom: 18px;
}


/* Buttons */

.stButton button {
    background-color: #8e75ad;
    color: white;
    border: none;
    border-radius: 9px;
}

.stButton button:hover {
    background-color: #72578f;
    color: white;
}


/* Footer */

.footer {
    text-align: center;
    color: #927fa8;
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# APPLICATION HEADING
# --------------------------------------------------

st.markdown(
    '<div class="main-heading">✈️ Travel Expense Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">Plan your journeys. Track your spending. Enjoy every moment.</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# DESTINATION IMAGE SLIDER
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Explore Beautiful Destinations</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">A little inspiration for your next adventure.</div>',
    unsafe_allow_html=True
)


slider_html = """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
}

.slider {
    position: relative;
    width: 100%;
    height: 390px;
    overflow: hidden;
    border-radius: 18px;
}

.slide {
    display: none;
    width: 100%;
    height: 100%;
    position: relative;
}

.slide.active {
    display: block;
}

.slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.caption {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 35px 25px;
    color: white;
    background: linear-gradient(
        transparent,
        rgba(0,0,0,0.75)
    );
}

.caption h2 {
    margin: 0 0 7px 0;
    font-size: 27px;
}

.caption p {
    margin: 0;
    font-size: 15px;
}

.arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    border-radius: 50%;
    width: 42px;
    height: 42px;
    font-size: 23px;
    cursor: pointer;
    background: rgba(255,255,255,0.85);
    color: #55416d;
}

.previous {
    left: 15px;
}

.next {
    right: 15px;
}

.dots {
    position: absolute;
    bottom: 15px;
    right: 25px;
    display: flex;
    gap: 8px;
}

.dot {
    width: 9px;
    height: 9px;
    background: rgba(255,255,255,0.6);
    border-radius: 50%;
    cursor: pointer;
}

.dot.active {
    background: white;
    width: 23px;
    border-radius: 10px;
}

</style>

</head>

<body>

<div class="slider">

    <div class="slide active">
        <img src="https://images.unsplash.com/photo-1514282401047-d79a71a590e8">
        <div class="caption">
            <h2>Maldives</h2>
            <p>Escape to turquoise waters and peaceful island resorts.</p>
        </div>
    </div>

    <div class="slide">
        <img src="https://images.unsplash.com/photo-1533105079780-92b9be482077">
        <div class="caption">
            <h2>Santorini, Greece</h2>
            <p>Discover beautiful coastlines and unforgettable sunsets.</p>
        </div>
    </div>

    <div class="slide">
        <img src="https://images.unsplash.com/photo-1531366936337-7c912a4589a7">
        <div class="caption">
            <h2>Switzerland</h2>
            <p>Find your peace among mountains and breathtaking views.</p>
        </div>
    </div>

    <div class="slide">
        <img src="https://images.unsplash.com/photo-1537996194471-e657df975ab4">
        <div class="caption">
            <h2>Bali, Indonesia</h2>
            <p>Experience tropical beauty, culture and adventure.</p>
        </div>
    </div>

    <button class="arrow previous" onclick="changeSlide(-1)">&#10094;</button>
    <button class="arrow next" onclick="changeSlide(1)">&#10095;</button>

    <div class="dots">
        <span class="dot active" onclick="showSlide(0)"></span>
        <span class="dot" onclick="showSlide(1)"></span>
        <span class="dot" onclick="showSlide(2)"></span>
        <span class="dot" onclick="showSlide(3)"></span>
    </div>

</div>

<script>

let currentSlide = 0;

const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");

function showSlide(index) {

    slides[currentSlide].classList.remove("active");
    dots[currentSlide].classList.remove("active");

    currentSlide = (index + slides.length) % slides.length;

    slides[currentSlide].classList.add("active");
    dots[currentSlide].classList.add("active");

}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

setInterval(function() {
    changeSlide(1);
}, 5000);

</script>

</body>
</html>
"""

components.html(slider_html, height=410)


# --------------------------------------------------
# QUICK ACCESS SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Your Travel Workspace</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Everything you need to manage your travel expenses.</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


# My Trips Card

with col1:

    with st.container(border=True, key="my_trips_card"):

        st.markdown("### 🧳 My Trips")

        st.write("Manage your journeys and destinations.")

        st.page_link(
            "pages/My_Trips.py",
            label="View My Trips",
            icon="🧳"
        )


# Add Expense Card

with col2:

    with st.container(border=True, key="add_expense_card"):

        st.markdown("### 💳 Add Expense")

        st.write("Record your travel spending easily.")

        st.page_link(
            "pages/Add_Expense.py",
            label="Add Expense",
            icon="➕"
        )


# Reports Card

with col3:

    with st.container(border=True, key="reports_card"):

        st.markdown("### 📊 Reports")

        st.write("Analyze your expenses and spending.")

        st.page_link(
            "pages/Reports.py",
            label="View Reports",
            icon="📊"
        )


# Budget Prediction Card

with col4:

    with st.container(border=True, key="budget_prediction_card"):

        st.markdown("### 🔮 Budget Prediction")

        st.write("Predict your travel expenses and manage your budget.")

        st.page_link(
            "pages/Budget_Prediction.py",
            label="View Prediction",
            icon="🔮"
        )


# --------------------------------------------------
# TRAVEL INSPIRATION GALLERY
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Travel Inspiration</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Some places are meant to be explored.</div>',
    unsafe_allow_html=True
)


# First row

gallery1, gallery2, gallery3 = st.columns(3)

with gallery1:

    st.image(
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        use_container_width=True
    )

    st.markdown(
        '<div class="inspiration-title">Mountain Adventures</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inspiration-caption">Take the scenic route and find your peace.</div>',
        unsafe_allow_html=True
    )


with gallery2:

    st.image(
        "https://images.unsplash.com/photo-1519046904884-53103b34b206",
        use_container_width=True
    )

    st.markdown(
        '<div class="inspiration-title">Beach Escapes</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inspiration-caption">Let the waves wash your worries away.</div>',
        unsafe_allow_html=True
    )


with gallery3:

    st.image(
        "https://images.unsplash.com/photo-1516483638261-f4dbaf036963",
        use_container_width=True
    )

    st.markdown(
        '<div class="inspiration-title">European Getaways</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inspiration-caption">Wander through beautiful streets and new cultures.</div>',
        unsafe_allow_html=True
    )


# Second row

st.markdown("<br>", unsafe_allow_html=True)

gallery4, gallery5, empty_column = st.columns(3)

with gallery4:

    st.image(
        "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
        use_container_width=True
    )

    st.markdown(
        '<div class="inspiration-title">Desert Wonders</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inspiration-caption">Discover golden dunes and the magic of endless horizons.</div>',
        unsafe_allow_html=True
    )


with gallery5:

    st.image(
        "https://images.unsplash.com/photo-1448375240586-882707db888b",
        use_container_width=True
    )

    st.markdown(
        '<div class="inspiration-title">Forest Retreats</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="inspiration-caption">Find calm in the beauty of nature and green landscapes.</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# TRAVEL QUOTES
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">A Little Travel Motivation</div>',
    unsafe_allow_html=True
)

quote1, quote2, quote3 = st.columns(3)

with quote1:

    with st.container(border=True):

        st.markdown("### 🌸")
        st.markdown("*“Collect moments, not things.”*")
        st.caption("A beautiful life is made of experiences.")


with quote2:

    with st.container(border=True):

        st.markdown("### 🦋")
        st.markdown("*“Adventure is calling.”*")
        st.caption("Sometimes the best answer is to go.")


with quote3:

    with st.container(border=True):

        st.markdown("### 💜")
        st.markdown("*“The world is too beautiful to stay in one place.”*")
        st.caption("Dream big. Travel far. Live fully.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Made with 💜 for every journey.<br>
    Travel Expense Manager
</div>
""", unsafe_allow_html=True)
