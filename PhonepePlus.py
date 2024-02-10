import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

icon = Image.open('C:/Users/matfr/OneDrive/Project/Second Project/1.png')
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | Mathew",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Mathew*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.markdown("<h1 style='text-align: center;'>Phonepe Pulse Data Visualization</h1>", unsafe_allow_html=True)

# Your Streamlit app content goes here

# Run the app
if __name__ == "__main__":
    st.write("Phonepe Pulse Data Visualization")


with st.sidebar:
    selected = option_menu("Menu", ["Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})


if selected == "About":
    st.image('C:/Users/matfr/OneDrive/Project/Second Project/1.png')
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image('C:/Users/matfr/OneDrive/Project/Second Project/1.png')


import altair as alt
import streamlit as st
import mysql.connector
import pandas as pd

# Assuming 'selected' is defined before this code snippet

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))

    if Type == "Transactions":
        mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="Mattpop", database="Phonepe")
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM aggre_transaction;")
        result = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(result, columns=columns)

        cursor.close()
        mydb.close()

        # Filter by selected years and quarter
        selected_years = st.multiselect("Select Years", df['Years'].unique())
        selected_quarters = st.multiselect("Select Quarters", df['Quarter'].unique())

        if selected_years and selected_quarters:
            df_filtered = df[(df['Years'].isin(selected_years)) & (df['Quarter'].isin(selected_quarters))]
        elif selected_years:
            df_filtered = df[df['Years'].isin(selected_years)]
        elif selected_quarters:
            df_filtered = df[df['Quarter'].isin(selected_quarters)]
        else:
            df_filtered = df

        # Group by 'States' and sum 'Transaction_Amount'
        df_grouped = df_filtered.groupby('States')['Transaction_Amount'].sum().reset_index()

        # Sort DataFrame by total 'Transaction_Amount' column in descending order
        df_sorted = df_grouped.sort_values(by='Transaction_Amount', ascending=False)

        # Create a bar chart using Altair
        chart = alt.Chart(df_sorted).mark_bar().encode(
            x='Transaction_Amount:Q',
            y=alt.Y('States:N', sort='-x'),
            tooltip=['States', 'Transaction_Amount']
        ).properties(
            width=600,
            height=400
        )

        # Split the screen into two columns
        col1, col2 = st.columns(2)

        # Display the resulting DataFrame in the left column
        col1.dataframe(df_sorted)

        # Display the chart in the right column
        col2.altair_chart(chart, use_container_width=True)
        
        
    if Type == "Users":
        mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="Mattpop", database="Phonepe")
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM aggre_user;")
        result = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(result, columns=columns)

        cursor.close()
        mydb.close()

        # Filter by selected years and quarter
        selected_years = st.multiselect("Select Years", df['Years'].unique())
        selected_quarters = st.multiselect("Select Quarters", df['Quarter'].unique())

        if selected_years and selected_quarters:
            df_filtered = df[(df['Years'].isin(selected_years)) & (df['Quarter'].isin(selected_quarters))]
        elif selected_years:
            df_filtered = df[df['Years'].isin(selected_years)]
        elif selected_quarters:
            df_filtered = df[df['Quarter'].isin(selected_quarters)]
        else:
            df_filtered = df

        
        df_grouped = df_filtered.groupby('States')['Transaction_Count'].sum().reset_index()

        # Sort DataFrame by total 'Transaction_Amount' column in descending order
        df_sorted = df_grouped.sort_values(by='Transaction_Count', ascending=False)

        # Create a bar chart using Altair
        chart = alt.Chart(df_sorted).mark_bar().encode(
            x='Transaction_Count:Q',
            y=alt.Y('States:N', sort='-x'),
            tooltip=['States', 'Transaction_Count']
        ).properties(
            width=600,
            height=400
        )

        # Split the screen into two columns
        col1, col2 = st.columns(2)

        # Display the resulting DataFrame in the left column
        col1.dataframe(df_sorted)

        # Display the chart in the right column
        col2.altair_chart(chart, use_container_width=True)




# Function to fetch data from MySQL database
def fetch_data(table_name):
    mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="Mattpop", database="Phonepe")
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    cursor.close()
    mydb.close()
    return df


# Streamlit main section
if selected == "Explore Data":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    column1, column2 = st.columns([1, 1.5], gap="large")

    # Handling "Transactions" type
    if Type == "Transactions":
        st.write("Displaying Transactions Map")
        # Fetch data from the aggre_User table
        df = fetch_data("aggre_transaction")

        # Create the choropleth map
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Amount',
            color_continuous_scale='greens',
            title='Transaction Amount by State'
        )

        fig.update_geos(fitbounds="locations", visible=False)

        # Show the choropleth map
        st.plotly_chart(fig)

        # Additional query for Users type
        df_top_10 = df.sort_values(by='Transaction_Amount', ascending=False).head(10)

        # Display the top 10 rows
        st.write("Top 10 rows by Transaction_Amount:")
        st.write(df_top_10)

        # Create a Streamlit data table for the sum of 'Transaction_Count' in brand-wise states
        fig_sunburst = px.sunburst(df, path=['Transaction_Type', 'States'], values='Transaction_Amount',
                                   title='Sum of Transaction_Amount in Transaction_Type')
        st.plotly_chart(fig_sunburst)

    # Handling "Users" type
    elif Type == "Users":
        st.write("Displaying Users Map")
        # Fetch data from the aggre_User table
        df = fetch_data("aggre_User")

        # Create the choropleth map
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Count',
            color_continuous_scale='greens',
            title='Transaction Count by State'
        )

        fig.update_geos(fitbounds="locations", visible=False)

        # Show the choropleth map
        st.plotly_chart(fig)

        # Additional query for Users type
        df_top_10 = df.sort_values(by='Transaction_Count', ascending=False).head(10)

        # Display the top 10 rows
        st.write("Top 10 rows by Transaction_Count:")
        st.write(df_top_10)

        # Create a Streamlit data table for the sum of 'Transaction_Count' in brand-wise states
        fig_sunburst = px.sunburst(df, path=['Brands', 'States'], values='Transaction_Count',
                                   title='Sum of Transaction_Count in Brand Wise States')
        st.plotly_chart(fig_sunburst)