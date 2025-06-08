This is a expense tracker I made with python and sqllite relational database. This program lets users make a user and then add, view, and delete their expenses. Also this uses a joins to make users able to view all the expesnes from all the users.

My use was to track my expenses with my wife and I to make sure we were in budget every month. 


Software Demo Video https://youtu.be/nSjXvl0NwIo

# Relational Database

This uses SQLlite which is a serverless database that stores data into a local file like Expenses.db. 

The database has two tables users and expenses. They are used to store the infomation from the users. The users table is used to store items for diffrent accounts. The expenses table stores all the entries the users made like the id, date, expenses, and amount. 

# Development Environment

I used python and SQLlite in VS code to make the expense tracker. I used prettytable to make the table in the console look nicer and it was easier to use then making my own. I used datetime to mark the date users inputed information. 

# Useful Websites


- Oracle https://www.oracle.com/databasewhat-is-a-relational-database/
- SQLite https://www.sqlite.org/docs.html

# Future Work

- I want to make it so I dont have to delete the db after everytime I want a new database. So I want to add a function to make more databases in the future and save them on my computer so I can track all my expenses through multible months.
- Maybe if I let others use the expense tracker I can add passwords to each user to make them more secure and make it so only certain users can see all the expesnses.
- Add a weekly or yearly expenses table to show more data then just the month. And so people can track how much they spend in a year or week or whatever they need.