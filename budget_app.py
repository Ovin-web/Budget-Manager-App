import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "Budget_data.json"

# ---------- Data Functions ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if "currency" not in data:
                data["currency"] = "USD"
            return data
    except:
        return {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def clear_all_data():
    data = {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}
    save_data(data)
    st.success("All data cleared!")

# ---------- UI Functions ----------

def add_income(data):
    with st.form("Add Income"):
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        source = st.text_input("Source")
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add Income")
        if submitted:
            data["income"].append({"amount": amount, "source": source, "date": str(date)})
            save_data(data)
            st.success("Income added!")

def add_expense(data):
    with st.form("Add Expense"):
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.text_input("Category")
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            total_exp = sum(item["amount"] for item in data["expenses"])
            if data["budget_limit"] and (total_exp + amount > data["budget_limit"]):
                st.warning("⚠️ This exceeds your budget limit!")
            data["expenses"].append({"amount": amount, "category": category, "date": str(date)})
            save_data(data)
            st.success("Expense added!")

def add_saving(data):
    with st.form("Add Saving"):
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        goal = st.text_input("Goal Name")
        submitted = st.form_submit_button("Add Saving")
        if submitted:
            data["savings"].append({"goal": goal, "amount": amount})
            save_data(data)
            st.success("Saving added!")

def set_currency(data):
    currency = st.text_input("Enter preferred currency (USD, EUR, etc.):", data.get("currency", "USD"))
    if st.button("Set Currency"):
        data["currency"] = currency.upper()
        save_data(data)
        st.success(f"Currency set to {currency.upper()}")

def set_budget_limit(data):
    limit = st.number_input("Set monthly budget limit:", min_value=0.0, format="%.2f")
    if st.button("Set Budget Limit"):
        data["budget_limit"] = limit
        save_data(data)
        st.success("Budget limit updated.")

def show_report(data):
    st.subheader("📊 Budget Report")
    currency = data["currency"]
    total_income = sum(item["amount"] for item in data["income"])
    total_expenses = sum(item["amount"] for item in data["expenses"])
    total_savings = sum(item["amount"] for item in data["savings"])
    remaining = total_income - total_expenses - total_savings

    st.markdown(f"""
    - 💰 **Total Income:** {total_income:.2f} {currency}
    - 📉 **Total Expenses:** {total_expenses:.2f} {currency}
    - 🏦 **Total Savings:** {total_savings:.2f} {currency}
    - 💵 **Remaining Balance:** {remaining:.2f} {currency}
    """)

    if st.checkbox("Show Transactions"):
        with st.expander("Income"):
            st.json(data["income"])
        with st.expander("Expenses"):
            st.json(data["expenses"])
        with st.expander("Savings"):
            st.json(data["savings"])

# ---------- Main App ----------

st.set_page_config(page_title="Budget Manager", page_icon="💼")
st.title("💼 Budget Manager App")

data = load_data()

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Income", "Add Expense", "Add Savings", "Settings", "Clear All"])

if menu == "Dashboard":
    show_report(data)

elif menu == "Add Income":
    add_income(data)

elif menu == "Add Expense":
    add_expense(data)

elif menu == "Add Savings":
    add_saving(data)

elif menu == "Settings":
    set_currency(data)
    set_budget_limit(data)

elif menu == "Clear All":
    if st.button("Clear All Budget Data"):
        clear_all_data()
