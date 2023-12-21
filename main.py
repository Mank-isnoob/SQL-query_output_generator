import base64
import streamlit as st
import plotly.express as px

df = px.data.iris()





page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}


[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)







import os
os.environ['OPENAI_API_KEY']='ENTER Your Key'
import sqlite3

import streamlit as st

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()


import numpy as np
import pandas as pd
import sqlite3
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import create_sql_query_chain
df = pd.read_csv("organizations-100.csv")

df.rename(columns={'UserIndex': 'UserIndex',
                   'Organization Id': 'Organization_Id',
                    'Name' : 'Name',
                   'Website' : 'Website',
                   'Country' : 'Country',
                   'Description' : 'Description',
                   'Founded' : 'Founded',
                   'Industry' : 'Industry',
                   'Number of employees':'Number_of_employees'}, inplace=True)

conn = sqlite3.connect('sample_db.sqlite')
c =conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user_database (UserIndex int, Organization_Id text, Name text, Website text, Country text, Description text, Founded int, Industry text, Number_of_employees int)')
conn.commit()

df.to_sql('user_database', conn, if_exists='replace', index = False)

#c.execute('''SELECT * FROM user_database LIMIT 100''')

for row in c.fetchall():
     print (row)


read_sql_query('SELECT * FROM user_database LIMIT 10;',"sample_db.sqlite")

input_db = SQLDatabase.from_uri('sqlite:///sample_db.sqlite')
llm_1 = OpenAI(temperature=0)
db_agent = create_sql_query_chain(llm_1,input_db)

#st.set_page_config(page_title="SQL generation")
st.header("Ask your SQL - Database - Custom")
user_question=st.text_input("Give a prompt for sql query generation")

if user_question is not None and user_question!="":
    st.subheader(user_question)
    with st.spinner(text="In Progress..."):

        response=db_agent.invoke({"question":user_question})

        st.subheader("Your requested query: ")
        st.write(response)

        st.subheader("Your Output: ")
        st.write(input_db.run(response))








