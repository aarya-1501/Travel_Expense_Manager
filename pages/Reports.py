
import streamlit as st
import pandas as pd
import plotly.express as px
import io


from database.database import (
    create_tables,
    get_all_expenses,
    get_all_trips
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Reports | Travel Expense Manager",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

create_tables()


# --------------------------------------------------
# CUSTOM CSS - LAVENDER THEME
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

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
section.main > div,
.block-container {
    padding-top: 0 !important;
}

.stApp {
    background-color: #faf8ff;
}

.block-container {
    max-width: 1250px;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-bottom: 2rem !important;
}

.main-heading {
    text-align: center;
    color: #55416d;
    font-size: 38px;
    font-weight: 700;
    padding-top: 5px;
    margin-bottom: 5px;
}

.sub-heading {
    text-align: center;
    color: #88769f;
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

/* Metric Cards */

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e9e0f2;
    border-radius: 15px;
    padding: 20px;
}

[data-testid="stMetricLabel"] {
    color: #88769f;
}

[data-testid="stMetricValue"] {
    color: #55416d;
    font-weight: 700;
}

/* Download Buttons */

.stDownloadButton > button {
    background-color: #8e75ad;
    color: white;
    border: 1px solid #8e75ad;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #72578f;
    color: white;
    border: 1px solid #72578f;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #e9e0f2;
    border-radius: 12px;
}

/* Information Boxes */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Manage Expenses Button */

[data-testid="stPageLink-NavLink"] {
    background-color: #eee6f7 !important;
    color: #55416d !important;
    border: 2px solid #8e75ad !important;
    border-radius: 13px !important;
    padding: 14px 24px !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stPageLink-NavLink"]:hover {
    background-color: #e3d5f2 !important;
    border: 2px solid #72578f !important;
    color: #55416d !important;
}

/* Footer */

.footer {
    text-align: center;
    color: #88769f;
    font-size: 13px;
    padding-top: 30px;
    padding-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-heading">📑 Expense Reports</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">'
    'Analyze your travel expenses and spending patterns.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# REPORTS OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Reports Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Explore your travel spending, analyze expenses, '
    'and track your budgets.'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Your reports provide a complete overview of your "
    "travel activities, expenses, and budget utilization."
)


# --------------------------------------------------
# RETRIEVE TRIPS AND EXPENSES
# --------------------------------------------------

trips = get_all_trips()
expenses = get_all_expenses()

trip_df = pd.DataFrame(
    [dict(trip) for trip in trips]
) if trips else pd.DataFrame()

expense_df = pd.DataFrame(
    [dict(expense) for expense in expenses]
) if expenses else pd.DataFrame()


# --------------------------------------------------
# PREPARE EXPENSE DATA
# --------------------------------------------------

if not expense_df.empty:

    # Convert expense amounts into numeric values.
    expense_df["amount"] = pd.to_numeric(
        expense_df["amount"],
        errors="coerce"
    ).fillna(0)

    # Handle missing category names.
    expense_df["category"] = (
        expense_df["category"]
        .fillna("Uncategorized")
        .replace("", "Uncategorized")
    )

    # Convert expense dates safely.
    expense_df["expense_date"] = pd.to_datetime(
        expense_df["expense_date"],
        errors="coerce"
    ).dt.date

    # Remove invalid dates from the daily report later.
    expense_df["expense_date"] = expense_df[
        "expense_date"
    ].astype("object")


# --------------------------------------------------
# CALCULATE OVERALL SUMMARY
# --------------------------------------------------

total_trips = len(trip_df)

if not trip_df.empty:

    trip_df["budget"] = pd.to_numeric(
        trip_df["budget"],
        errors="coerce"
    ).fillna(0)

    total_budget = float(trip_df["budget"].sum())

else:

    total_budget = 0.0


if not expense_df.empty:

    total_expenses = float(
        expense_df["amount"].sum()
    )

else:

    total_expenses = 0.0


remaining_balance = total_budget - total_expenses


# --------------------------------------------------
# OVERALL EXPENSE SUMMARY
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📊 Overall Expense Summary</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Trips",
        total_trips
    )

with col2:
    st.metric(
        "Total Budget",
        f"₹{total_budget:,.2f}"
    )

with col3:
    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}"
    )

with col4:
    st.metric(
        "Remaining Balance",
        f"₹{remaining_balance:,.2f}"
    )


if total_trips == 0:
    st.info("You haven't created any trips yet.")

if total_expenses == 0:
    st.info("No expenses have been recorded yet.")


# --------------------------------------------------
# CATEGORY-WISE EXPENSE REPORT
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📂 Category-wise Expense Report</div>',
    unsafe_allow_html=True
)

category_report = pd.DataFrame(
    columns=["Expense Category", "Total Amount (₹)"]
)

if not expense_df.empty:

    category_report = (
        expense_df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    category_report.columns = [
        "Expense Category",
        "Total Amount (₹)"
    ]

    category_report = category_report.sort_values(
        "Total Amount (₹)",
        ascending=False
    )

    st.dataframe(
        category_report,
        use_container_width=True,
        hide_index=True
    )

    if category_report["Total Amount (₹)"].sum() > 0:

        fig = px.pie(
            category_report,
            names="Expense Category",
            values="Total Amount (₹)",
            title="Spending Distribution by Category",
            hole=0.4
        )

        fig.update_layout(
            paper_bgcolor="#faf8ff",
            plot_bgcolor="#faf8ff",
            font_color="#55416d"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("There is no positive expense amount to display in the category chart.")

else:

    st.info("No expense records available for this report.")


# --------------------------------------------------
# DAILY EXPENSE REPORT
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📅 Daily Expense Report</div>',
    unsafe_allow_html=True
)

daily_report = pd.DataFrame(
    columns=["Expense Date", "Total Amount (₹)"]
)

if not expense_df.empty:

    valid_daily_expenses = expense_df.dropna(
        subset=["expense_date"]
    ).copy()

    if not valid_daily_expenses.empty:

        daily_report = (
            valid_daily_expenses
            .groupby("expense_date")["amount"]
            .sum()
            .reset_index()
        )

        daily_report.columns = [
            "Expense Date",
            "Total Amount (₹)"
        ]

        daily_report = daily_report.sort_values(
            "Expense Date"
        )

        st.dataframe(
            daily_report,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No valid expense dates are available for daily analysis.")

else:

    st.info("No expense records available for daily analysis.")


# --------------------------------------------------
# TRIP-WISE BUDGET UTILIZATION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">✈️ Trip-wise Budget Utilization</div>',
    unsafe_allow_html=True
)

budget_report = pd.DataFrame(
    columns=[
        "Trip Name",
        "Destination",
        "Total Budget (₹)",
        "Total Expenses (₹)",
        "Remaining Budget (₹)",
        "Budget Used (%)"
    ]
)

if not trip_df.empty:

    if not expense_df.empty:

        trip_expense_summary = (
            expense_df.groupby("trip_id")["amount"]
            .sum()
            .reset_index()
        )

    else:

        trip_expense_summary = pd.DataFrame(
            columns=["trip_id", "amount"]
        )

    budget_report = trip_df.merge(
        trip_expense_summary,
        on="trip_id",
        how="left"
    )

    budget_report["amount"] = (
        budget_report["amount"].fillna(0)
    )

    budget_report["Remaining Budget (₹)"] = (
        budget_report["budget"] - budget_report["amount"]
    )

    # Avoid division by zero when a trip budget is zero.
    budget_report["Budget Used (%)"] = (
        budget_report["amount"]
        .div(
            budget_report["budget"].replace(
                0,
                float("nan")
            )
        )
        .mul(100)
        .fillna(0)
        .round(2)
    )

    budget_report = budget_report[
        [
            "trip_name",
            "destination",
            "budget",
            "amount",
            "Remaining Budget (₹)",
            "Budget Used (%)"
        ]
    ].copy()

    budget_report.columns = [
        "Trip Name",
        "Destination",
        "Total Budget (₹)",
        "Total Expenses (₹)",
        "Remaining Budget (₹)",
        "Budget Used (%)"
    ]

    st.dataframe(
        budget_report,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # BUDGET VS ACTUAL CHART
    # --------------------------------------------------

    st.markdown(
        '<div class="section-heading">'
        '📊 Trip Budget vs Actual Expenses'
        '</div>',
        unsafe_allow_html=True
    )

    budget_chart_df = budget_report[
        [
            "Trip Name",
            "Total Budget (₹)",
            "Total Expenses (₹)"
        ]
    ].melt(
        id_vars="Trip Name",
        var_name="Budget Type",
        value_name="Amount"
    )

    fig = px.bar(
        budget_chart_df,
        x="Trip Name",
        y="Amount",
        color="Budget Type",
        barmode="group",
        title="Trip Budget vs Actual Expenses",
        text_auto=".2s"
    )

    fig.update_layout(
        paper_bgcolor="#faf8ff",
        plot_bgcolor="#faf8ff",
        font_color="#55416d"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No trips available for budget analysis.")


# --------------------------------------------------
# COMPLETE EXCEL REPORT DOWNLOAD
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📥 Download Complete Report</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Download all your travel information in one Excel workbook, '
    'organized into separate sheets.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# OVERALL SUMMARY SHEET
# --------------------------------------------------

summary_report = pd.DataFrame({
    "Metric": [
        "Total Trips",
        "Total Budget (₹)",
        "Total Expenses (₹)",
        "Remaining Balance (₹)"
    ],
    "Value": [
        total_trips,
        total_budget,
        total_expenses,
        remaining_balance
    ]
})


# --------------------------------------------------
# GENERATE EXCEL WORKBOOK
# --------------------------------------------------

excel_buffer = io.BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    # Sheet 1: Overall Summary

    summary_report.to_excel(
        writer,
        index=False,
        sheet_name="Overall Summary"
    )

    # Sheet 2: All Expenses

    if not expense_df.empty:

        expense_df.to_excel(
            writer,
            index=False,
            sheet_name="All Expenses"
        )

    else:

        pd.DataFrame(
            columns=["No Expense Records Available"]
        ).to_excel(
            writer,
            index=False,
            sheet_name="All Expenses"
        )

    # Sheet 3: Category Report

    category_report.to_excel(
        writer,
        index=False,
        sheet_name="Category Report"
    )

    # Sheet 4: Daily Report

    daily_report.to_excel(
        writer,
        index=False,
        sheet_name="Daily Report"
    )

    # Sheet 5: Trip Budget Report

    budget_report.to_excel(
        writer,
        index=False,
        sheet_name="Trip Budget Report"
    )

    # --------------------------------------------------
    # ADJUST EXCEL COLUMN WIDTHS
    # --------------------------------------------------

    for sheet in writer.sheets.values():

        for column_cells in sheet.columns:

            max_length = 0

            column_letter = (
                column_cells[0].column_letter
            )

            for cell in column_cells:

                if cell.value is not None:

                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

            sheet.column_dimensions[
                column_letter
            ].width = min(max_length + 4, 40)


# --------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------

st.download_button(
    label="📊 Download Complete Travel Report (Excel)",
    data=excel_buffer.getvalue(),
    file_name="Complete_Travel_Expense_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)


# --------------------------------------------------
# MANAGE EXPENSES BUTTON - ABOVE FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📝 Manage Your Expenses</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Want to edit or delete an existing expense? '
    'Manage all your recorded expenses here.'
    '</div>',
    unsafe_allow_html=True
)

st.page_link(
    "pages/Manage_Expenses.py",
    label="📝 Manage Expenses"
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
