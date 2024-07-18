import pandas as pd
import csv
from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORY = {'I': 'Income', 'E': 'Expense'}

def get_date(prompt, allow_default=True):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print('Enter a valid date format: %d-%m-%Y')
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input('Enter the amount: '))
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORY:
        return CATEGORY[category]

    print('Invalid entry. Please select I for Income and E for Expense')
    return get_category()

def get_description():
    return input('Enter the description (optional): ')

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print('Entry added successfully')

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=CSV.FORMAT)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given date range.')
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print('\nSummary:')
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Total Savings: ${(total_income - total_expense):.2f}")
        
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date('Enter the date of the transaction (dd-mm-yyyy): ', allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

# Initialize the CSV file (create if it doesn't exist)
CSV.initialize_csv()

# Example usage: Add an entry
# CSV.add_entry('17-07-2024', 100, 'Groceries', 'Bought vegetables and fruits')
CSV.get_transaction("01-01-2023", "30-07-2024")
# add()
