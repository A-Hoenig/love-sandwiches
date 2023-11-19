import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from user.
    Run a while loop to collect a valid string of data from user
    via terminal. must be a string og 6 comma seperated values.
    Loop repeates until valid data is recieved
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(",")
       
        if validate_data(sales_data):
            print('Valid Data!')
            break
    return sales_data
        

def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
            print(f'Invalid Data: {e}, please try again. \n')
            return False
    
    return True    

def update_worksheet(data, worksheet):
    """
    recives a list of integers to be inserted ina worksheet
    updating the relevant workheet with the new data
    """
    print(f'Updating {worksheet} data...\n')
    target_worksheet = SHEET.worksheet(worksheet)
    target_worksheet.append_row(data)
    print(f'{worksheet} worksheet updated successfully. \n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each sandwich type

    Surplus is defined as stock - sales:
    positive surplus indicates waste (thrown away stock)
    negative surplus indicates extra fresh made when stock ran out
    """
    print('Calculating surplus data ... \n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
        
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    """
    collects columns of data from sales, returning the last 5 entries
    for each sandwhich and then returns the data as a list of lists
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    calculate the average stock for each type and add 10%
    """
    print("Calculatying new stock recommendation")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
        
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print('\nWelcome to LoveSandwiches Data Automation\n')
main()