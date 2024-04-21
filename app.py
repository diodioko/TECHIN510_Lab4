import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from db import Database

load_dotenv()

# Function to fetch books based on search and sorting criteria
def fetch_books(query, order_by, desc):
    with Database(os.getenv('DATABASE_URL')) as pg:
        order_direction = "DESC" if desc else "ASC"
        sql_query = f"""
        SELECT * FROM books
        WHERE name ILIKE %s OR description ILIKE %s
        ORDER BY {order_by} {order_direction}
        """
        df = pd.read_sql(sql_query, pg.con, params=(f'%{query}%', f'%{query}%'))
    return df

st.title('📘Book Search')

# User inputs for search and sorting
search_query = st.text_input("Search by name or description", "")
order_by = st.selectbox("Order by", options=["rating", "price"], index=0)
desc = st.checkbox("Descending order", value=True)

# Fetch data based on user input
if st.button('Search') or search_query:
    df = fetch_books(search_query, order_by, desc)
    if df.empty:
        st.write("No books found.")
    else:
        # Display the data in a container with a vertical scrollbar
        st.dataframe(df, 800, 400)  # You can adjust the height and width as needed
else:
    st.write("Enter a query and click search to filter the results.")

