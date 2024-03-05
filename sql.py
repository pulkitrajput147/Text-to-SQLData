import sqlite3

# Connect to sqlite
connection = sqlite3.connect("student.db")

# Create a cursor object in order to insert record, create table, retrieve
cursor = connection.cursor()

# Create the table
table_info = """
CREATE table STUDENT(NAME VARCHAR(25), CLASS INT,
SECTION VARCHAR(25), MARKS INT);

"""
cursor.execute(table_info)

# Insert some records in the table
cursor.execute(''' Insert Into STUDENT values('John',12,'CSE',85) ''')
cursor.execute(''' Insert Into STUDENT values('Marsh',12,'CSE',72) ''')
cursor.execute(''' Insert Into STUDENT values('Mac',12,'CSE',49) ''')
cursor.execute(''' Insert Into STUDENT values('Steve',11,'Economic',69) ''')
cursor.execute(''' Insert Into STUDENT values('warner',11,'Economic',84) ''')
cursor.execute(''' Insert Into STUDENT values('david',11,'Economic',44) ''')
cursor.execute(''' Insert Into STUDENT values('Harsh','10','History',45) ''')

# Display all the records
print("The records in the database are :")
data=cursor.execute(''' Select * FROM STUDENT''')

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()
