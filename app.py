# Importing necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

#Load all the environment variables
load_dotenv()

# Configure our api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and provide sql query as response
def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Function to get data from the database(via query)
def read_sql_query(sql,db):
    connection=sqlite3.connect(db)
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

# Defining the prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION , MARKS .\n\n
    For example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output  
    """
]

# Streamlit app
st.set_page_config(page_title="Retrieve SQL Data via Simple Text")
st.header("App to retrieve SQL data")
question=st.text_input("Input :", key="input")
submit=st.button("Fetch")

# if submit button is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)

    # Connect to the database and retrieve column names
    connection1 = sqlite3.connect("student.db")
    cursor1 = connection1.cursor()
    cursor1.execute("PRAGMA table_info(STUDENT)")
    column_names = [row[1] for row in cursor1.fetchall()]  # Get column names
    connection1.close()

    # retrieving the data from db
    data=read_sql_query(response,"student.db")

    # Assign column names to the dataframe
    df = pd.DataFrame(data, columns=column_names)

    # output
    st.subheader("Response :")
    st.dataframe(df)

