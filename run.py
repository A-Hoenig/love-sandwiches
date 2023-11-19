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
    print(values)
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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated successfully. \n')

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print('Updating surplus data...\n')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print('Surplus worksheet updated successfully. \n')
    
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



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print('\nWelcome to LoveSandwiches Data Automation\n')
main()