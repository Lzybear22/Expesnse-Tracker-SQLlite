import sqlite3
from datetime import datetime
from prettytable import PrettyTable  # For nice formatted table

# Connect to SQLite database file Expenses.db
# If the file doesn't exist, SQLite will create it
conn = sqlite3.connect('Expenses.db')
c = conn.cursor()  # Create a cursor object to execute commands

def create_tables():
    """
    Creates the necessary tables: users and expenses.
    If these tables already exist, does nothing.
    """
    # Create users table with columns:
    # id and username
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create 'expenses' table with columns:
    # id (primary key, auto-incremented),
    # user_id (foreign key referencing users.id),
    # date (text),
    # expense (text),
    # amount (real number),
    # total (running total, real number)
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT,
            expense TEXT,
            amount REAL,
            total REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Save changes to the database
    conn.commit()

def login():
    """
    Prompts for username input.
    Checks if user exists in users table.
    If yes, returns the existing user_id.
    If no, inserts new user and returns new user_id.
    """
    username = input("Enter your username: ")  # Get username from user
    
    # Check if this username already exists in the users table
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    
    if row:
        # If user found greet and return user_id
        print(f"Welcome back, {username}!")
        return row[0]
    else:
        # If user not found, insert a new user record
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        print(f"New user '{username}' registered.")
        # Return the id of the newly created user
        return c.lastrowid

def data_entry(user_id):
    """
    Adds a new expense entry for the logged-in user.
    Calculates the new running total after adding the expense.
    """
    date = str(datetime.now().date())  # Get current date as string in YYYY-MM-DD format
    
    expense = input('Enter the expense: ')  # Ask for expense description
    amount = float(input('Enter the amount spent: '))  # Ask for amount and convert to float
    
    # Retrieve the current total expenses amount for this user
    c.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    total = c.fetchone()[0] or 0  # If no expenses yet, total will be None
    
    total += amount  # Add current amount to total
    
    # Insert new row into expenses table with user_id, date, expense description, amount, and running total
    c.execute('INSERT INTO expenses (user_id, date, expense, amount, total) VALUES (?, ?, ?, ?, ?)',
              (user_id, date, expense, amount, total))
    
    # Save the change
    conn.commit()
    
    print("Expense added.")

def view_data(user_id):
    """
    Displays all expenses for the logged-in user as a formatted table.
    """
    # Select relevant columns for this user, ordered by id
    c.execute('SELECT id, date, expense, amount, total FROM expenses WHERE user_id = ? ORDER BY id', (user_id,))
    rows = c.fetchall()
    
    if rows:
        # Create a PrettyTable with appropriate headers
        table = PrettyTable(["ID", "Date", "Expense", "Amount", "Total"])
        
        # Add each row from the database to the table
        for row in rows:
            table.add_row(row)
        
        # Print the formatted table
        print(table)
    else:
        print("No expenses found for this user.")

def delete_data(user_id):
    """
    Deletes an expense entry by its ID for the logged-in user.
    After deletion, recalculates and updates the running totals for all remaining expenses.
    """
    rowid = input('Enter the ID of the expense to delete: ')  # Ask which expense to delete
    
    # Check if the expense exists for this user and get its amount
    c.execute('SELECT amount FROM expenses WHERE id = ? AND user_id = ?', (rowid, user_id))
    temp = c.fetchone()
    
    if temp is not None:
        # Delete the expense record from the table
        c.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (rowid, user_id))
        
        # Fetch all remaining expenses for this user ordered by id
        c.execute('SELECT id, amount FROM expenses WHERE user_id = ? ORDER BY id', (user_id,))
        rows = c.fetchall()
        
        running_total = 0  # Initialize running total
        # Update the total column for each expense in order
        for row in rows:
            running_total += row[1]  # Add amount to running total
            c.execute('UPDATE expenses SET total = ? WHERE id = ?', (running_total, row[0]))
        
        # Commit all updates
        conn.commit()
        
        print("Expense deleted and totals recalculated.")
    else:
        # If expense not found for given id and user tell user
        print("Expense not found.")

def view_all_users_expenses():
    """
    Displays expenses for all users.
    Shows username and all expense details in a combined table.
    """
    # SQL JOIN to get expenses along with username from users table
    query = '''
    SELECT expenses.id, users.username, expenses.date, expenses.expense, expenses.amount, expenses.total
    FROM expenses
    JOIN users ON expenses.user_id = users.id
    ORDER BY expenses.id
    '''
    c.execute(query)
    rows = c.fetchall()
    
    if rows:
        table = PrettyTable(["Expense ID", "Username", "Date", "Expense", "Amount", "Total"])
        for row in rows:
            table.add_row(row)
        print(table)
    else:
        print("No expenses found.")

def main():
    """
    Main program loop that:
    Creates tables if needed
    Handles user login/registration
    Displays menu for user interaction
    """
    create_tables()  # Ensure tables exist
    user_id = login()  # Log in or create user and get user_id
    
    while True:
        print("\n1. Add Expense \n2. View Your Expenses \n3. Delete a Row \n4. View All Users' Expenses \n5. Exit")
        
        try:
            inp = int(input("Input: "))  # Read user menu choice
        except ValueError:
            # Handle invalid input (not an integer)
            print("Please enter a valid number.")
            continue
        
        # Call corresponding functions based on user choice
        if inp == 1:
            data_entry(user_id)
        elif inp == 2:
            view_data(user_id)
        elif inp == 3:
            delete_data(user_id)
        elif inp == 4:
            view_all_users_expenses()
        elif inp == 5:
            print("Goodbye!")
            break  # Exit the loop and program
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()  # Run the main function when script is executed
    conn.close()  # Close database connection before exiting
