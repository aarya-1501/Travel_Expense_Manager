# ✈️ Travel Expense Manager

A web-based application built using Python and Streamlit to help users plan trips, track travel expenses, monitor budgets, and predict total trip spending.

## 🌟 Features

- **Trip Management:** Create and manage multiple trips with destinations, travel dates and budgets.
- **Expense Tracking:** Add, edit and delete expenses for individual trips.
- **Trip-wise Expense Organization:** View expenses separately for each trip.
- **Dashboard:** Monitor total expenses, trip activity and spending categories.
- **Search and Filters:** Search expenses and filter them by category.
- **Reports:** View category-wise, daily and trip-wise expense summaries.
- **Excel Export:** Download comprehensive travel expense reports in Excel format.
- **Budget Prediction:** Estimate final trip expenses using recorded spending and elapsed trip days.
- **Prediction History:** Save and review previous predictions.
- **Budget Monitoring:** Identify potential budget overruns and track budget utilization.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- OpenPyXL

## 📁 Project Structure

```text
Travel_Expense_Manager/
│
├── app.py
├── prediction.py
├── requirements.txt
│
├── database/
│   ├── database.py
│   └── travel_expenses.db
│
├── pages/
│   ├── Dashboard.py
│   ├── My_Trips.py
│   ├── Add_Expense.py
│   ├── Manage_Expenses.py
│   ├── Reports.py
│   └── Budget_Prediction.py
│
└── assets/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Travel_Expense_Manager
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🔮 Budget Prediction Logic

The application uses a rule-based mathematical approach to estimate final trip expenses.

It calculates average daily spending using recorded expenses and elapsed trip days, then projects the spending across the total trip duration.

The application also compares predicted expenses with the planned budget to identify potential budget overruns.

## 💾 Database

SQLite is used to store trip details, expense records and prediction history.

## 🎯 Project Objective

The objective of this project is to provide a simple and user-friendly platform for managing travel finances, organizing expenses and making better travel budget decisions.

---

**Made with 💜 for every journey.**