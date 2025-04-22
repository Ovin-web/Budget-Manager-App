import json
import os
from datetime import datetime

DATA_FILE = "Budget_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if "currency" not in data:
                data["currency"] = "USD"
            return data
    except (json.JSONDecodeError, IOError):
        print("Error loading data. Initializing empty budget.")
        return {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("Error saving data.")

def backup_data():
    try:
        if os.path.exists(DATA_FILE):
            os.rename(DATA_FILE, DATA_FILE + ".bak")
            print("Backup created successfully!")
        else:
            print("No data found to backup.")
    except OSError:
        print("Error creating backup.")

def restore_data():
    try:
        if os.path.exists(DATA_FILE + ".bak"):
            os.rename(DATA_FILE + ".bak", DATA_FILE)
            print("Data restored from backup successfully!")
        else:
            print("No backup found.")
    except OSError:
        print("Error restoring backup.")

def clear_all_data():
    confirm = input("Are you sure you want to **delete all data**? This cannot be undone (yes/no): ").strip().lower()
    if confirm == "yes":
        backup_data()
        data = {"income": [], "expenses": [], "savings": [], "budget_limit": None, "currency": "USD"}
        save_data(data)
        print("All data has been cleared.")
    else:
        print("Action cancelled.")

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Please enter in YYYY-MM-DD.")
        return None

def set_currency(data):
    currency = input("Enter your preferred currency (e.g., USD, EUR, GBP, JPY): ").strip().upper()
    if currency:
        data["currency"] = currency
        save_data(data)
        print(f"Currency set to {currency} successfully!")
    else:
        print("Invalid currency input.")

def add_income(data):
    try:
        amount = float(input(f"Enter income amount ({data['currency']}): "))
        source = input("Enter source of income: ")
        date = None
        while date is None:
            date = validate_date(input("Enter date (YYYY-MM-DD): "))
        data["income"].append({"amount": amount, "source": source, "date": date})
        save_data(data)
        print("Income added successfully.")
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")

def add_expense(data):
    try:
        amount = float(input(f"Enter expense amount ({data['currency']}): "))
        category = input("Enter category of expense: ")
        date = None
        while date is None:
            date = validate_date(input("Enter date (YYYY-MM-DD): "))
        budget_limit = data.get("budget_limit")
        total_expenses = sum(item["amount"] for item in data["expenses"])
        if budget_limit is not None and total_expenses + amount > budget_limit:
            print(f"Warning: This expense exceeds your budget limit of {budget_limit} {data['currency']}!")
        data["expenses"].append({"amount": amount, "category": category, "date": date})
        save_data(data)
        print("Expense added successfully.")
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")

def add_savings_goal(data):
    try:
        goal = input("Enter savings goal name: ")
        amount = float(input(f"Enter savings contribution amount ({data['currency']}): "))
        data["savings"].append({"goal": goal, "amount": amount})
        save_data(data)
        print("Savings contribution added successfully.")
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")

def edit_item(data, section):
    if section not in data or not data[section]:
        print(f"No items found in {section}.")
        return
    for idx, item in enumerate(data[section], start=1):
        print(f"{idx}. {item}")
    try:
        choice = int(input("Enter the number of the item you want to edit: "))
        if 1 <= choice <= len(data[section]):
            item = data[section][choice - 1]
            for key in item:
                new_val = input(f"Enter new value for '{key}' (leave blank to keep '{item[key]}'): ")
                if new_val:
                    item[key] = float(new_val) if isinstance(item[key], float) else new_val
            save_data(data)
            print("Item updated successfully.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def delete_item(data, section):
    if section not in data or not data[section]:
        print(f"No items found in {section}.")
        return
    for idx, item in enumerate(data[section], start=1):
        print(f"{idx}. {item}")
    try:
        choice = int(input("Enter the number of the item you want to delete: "))
        if 1 <= choice <= len(data[section]):
            removed = data[section].pop(choice - 1)
            save_data(data)
            print(f"Deleted: {removed}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def generate_report(data):
    currency = data["currency"]
    print("\n" + "-" * 40)
    print(f"📊 Budget Summary Report ({currency})")
    print("-" * 40)

    # Income
    print("\n💰 Income Transactions:")
    total_income = sum(item["amount"] for item in data["income"])
    if data["income"]:
        for item in data["income"]:
            print(f"📆 {item['date']} - {item['source']}: {item['amount']} {currency}")
        print(f"🔹 Total Income: {total_income:.2f} {currency}")
    else:
        print("No income records found.")

    # Expenses
    print("\n📉 Expense Transactions:")
    total_expenses = sum(item["amount"] for item in data["expenses"])
    if data["expenses"]:
        for item in data["expenses"]:
            print(f"📆 {item['date']} - {item['category']}: {item['amount']} {currency}")
        print(f"🔹 Total Expenses: {total_expenses:.2f} {currency}")
    else:
        print("No expense records found.")

    # Savings
    print("\n🏦 Savings Contributions:")
    total_savings = sum(item["amount"] for item in data["savings"])
    if data["savings"]:
        for item in data["savings"]:
            print(f"🎯 {item['goal']} - {item['amount']} {currency}")
        print(f"🔹 Total Saved: {total_savings:.2f} {currency}")
    else:
        print("No savings contributions found.")

    # Remaining Balance
    remaining = total_income - total_expenses - total_savings
    print("\n💡 Remaining Balance:")
    print(f"✅ {remaining:.2f} {currency}")
    print("-" * 40)

def main():
    data = load_data()
    while True:
        print(f"\nBudget Management System (Currency: {data['currency']})")
        print("1. Set Currency")
        print("2. Add Income")
        print("3. Add Expense")
        print("4. Add Savings Contribution")
        print("5. Edit Income")
        print("6. Edit Expense")
        print("7. Edit Savings")
        print("8. Delete Income")
        print("9. Delete Expense")
        print("10. Delete Savings")
        print("11. Generate Report")
        print("12. Clear All Data")
        print("13. Backup Data")
        print("14. Restore Data")
        print("15. Exit")

        choice = input("Enter your choice: ")
        if choice == "1": set_currency(data)
        elif choice == "2": add_income(data)
        elif choice == "3": add_expense(data)
        elif choice == "4": add_savings_goal(data)
        elif choice == "5": edit_item(data, "income")
        elif choice == "6": edit_item(data, "expenses")
        elif choice == "7": edit_item(data, "savings")
        elif choice == "8": delete_item(data, "income")
        elif choice == "9": delete_item(data, "expenses")
        elif choice == "10": delete_item(data, "savings")
        elif choice == "11": generate_report(data)
        elif choice == "12": clear_all_data()
        elif choice == "13": backup_data()
        elif choice == "14": restore_data()
        elif choice == "15":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
