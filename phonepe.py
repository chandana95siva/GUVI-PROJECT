import streamlit as st
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import io
import pandas as pd
import re
import requests
import mysql.connector
from datetime import datetime
import json
import os
import sqlite3
con = sqlite3.connect("phonepe.db")
mycursor = con.cursor()
# reading Csv file using pandas
agg_trans_df = pd.read_csv(r'AGGREGATED_TRANS.csv')
agg_user_df = pd.read_csv(r'AGGREGATED_USER.csv')
map_trans_df = pd.read_csv(r'Map_Trans.csv')
map_user_df = pd.read_csv(r'Map_User.csv')
top_trans_dist_df = pd.read_csv(r'Top_Trans_Districts.csv')
top_trans_pin_df = pd.read_csv(r'Top_Trans_pincode.csv')
top_user_dist_df = pd.read_csv(r'Top_User_districts.csv')
top_user_pin_df = pd.read_csv(r'Top_User_pincode.csv')

# creating option menu
with st.sidebar:
    image = Image.open('phonepe.png')
    st.image(image)    
    selected =option_menu(
    menu_title= None,
    options=["HOME","BASIC INSIGHTS","ANALYSIS"],
    icons= ["house","bar-chart","exclamation-circle"],
    menu_icon ="cast",
    default_index= 0,
)
    
   
if selected == "HOME":
    image = Image.open('phonepe.jpeg')
    st.image(image)    
    st.write('''The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.''')
    st.subheader(f"TECHNOLOGIES USED")
    st.write('''Github Cloning, Python, Pandas, MySQL,Streamlit, and Plotly.''')
    st.header(f"ABOUT THE PROJECT")
    st.write('''The Goal of this project is to extract data from the phonepe pulse Github repository,Transform and clean the data,insert it into a MySQL Database and create a live Geo visualization Dashboard using Streamlit,Plotly in python ''')
if selected == "BASIC INSIGHTS":
    st.title("BASIC INSIGHTS")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--","Top 10 states based on year and amount of transaction",
               "Least 10 states based on type and amount of transaction",
               "Top 10 mobile brands based on percentage of transaction",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and amount of transaction",
               "Least 10 Districts based on states and amount of transaction",
               "Least 10 registered-users based on Districts and states",
               "Top 10 transactions_type based on states and transaction_amount"]
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,metric_amount,Year,Quater FROM TOP_TRANSACTION_DISTRICTS GROUP By State ORDER By metric_amount DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transaction_amount','Year','Quater'])
        st.subheader("Top 10 states based on type and amount of transaction")
        st.bar_chart(data=df,x="State",y="Transaction_amount")
    elif select=="Least 10 states based on type and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,metric_amount,year,Quater FROM TOP_TRANSACTION_DISTRICTS GROUP By State ORDER By metric_amount ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transaction_amount','Year','Quater'])
        st.subheader("Least 10 states based on type and amount of transaction")
        st.bar_chart(data=df,x="State",y="Transaction_amount")    
    elif select=="Top 10 mobile brands based on percentage of transaction":
        mycursor.execute("SELECT DISTINCT Brand_name,UserPercentage FROM AGGREGATED_USER GROUP By Brand_name ORDER By UserPercentage DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['Brand_name','UserPercentage'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 mobile brands based on percentage of transaction")
            st.bar_chart(data=df,x="Brand_name",y="UserPercentage")
    elif select=="Top 10 Registered-users based on States and District":
        mycursor.execute("SELECT DISTINCT State,Districts,RegisteredUsers FROM TOP_USER_DISTRICTS GROUP By State,Districts ORDER By RegisteredUsers DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','RegisteredUser'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Registered-users based on States and District")
            st.bar_chart(data=df,x="State",y="RegisteredUser")
    elif select=="Top 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,metric_type,metric_amount FROM MAP_TRANSACTION GROUP By State,metric_type ORDER By metric_amount DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,x="State",y="Transaction_amount")
    elif select=="Least 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,metric_type,metric_amount FROM MAP_TRANSACTION GROUP By State,metric_type ORDER By metric_amount ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,x="State",y="Transaction_amount")
    elif select=="Least 10 registered-users based on Districts and states":
        mycursor.execute("SELECT DISTINCT State,Districts,RegisteredUsers FROM TOP_USER_DISTRICTS GROUP BY State,Districts ORDER By RegisteredUsers ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','RegisteredUser'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Least 10 registered-users based on Districts and states")
            st.bar_chart(data=df,x="State",y="RegisteredUser")
    elif select=="Top 10 transactions_type based on states and transaction_amount":
        mycursor.execute("SELECT DISTINCT State,Transaction_type,Transaction_amt FROM AGGREGATED_TRANSACTION GROUP By State,Transaction_type ORDER By Transaction_amt DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transaction_type','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 transactions_type based on states and transaction_amount")
            st.bar_chart(data=df,x="State",y="Transaction_amount")
if selected == "ANALYSIS":
    option = st.selectbox('**Select your option**',('All India', 'State wise','Top categories'))
    if option == 'All India':
        tab1, tab2 = st.tabs(['Transaction','User'])
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                in_trans_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_trans_yr')
            with col2:
                in_trans_qtr = st.selectbox('**Select Quater**', ('1','2','3','4'),key='in_trans_qtr')
            with col3:
                in_trans_typ = st.selectbox('**Select Transaction_type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='in_trans_typ')

#         # SQL Query

#         # Transaction Analysis bar chart query
        mycursor.execute(f"SELECT State, Transaction_amt FROM AGGREGATED_TRANSACTION WHERE Year = '{in_trans_yr}' AND Quater = '{in_trans_qtr}' AND Transaction_type = '{in_trans_typ}';")
        trns_tab_qry_rslt = mycursor.fetchall()
        df_trns_tab_qry_rslt = pd.DataFrame(np.array(trns_tab_qry_rslt), columns=['State', 'Transaction_amount'])
        df_trns_tab_qry_rslt1 = df_trns_tab_qry_rslt.set_index(pd.Index(range(1, len(df_trns_tab_qry_rslt)+1)))

        # Transaction Analysis table query
        mycursor.execute(f"SELECT State, Transaction_count, Transaction_amt FROM AGGREGATED_TRANSACTION WHERE Year = '{in_trans_yr}' AND Quater = '{in_trans_qtr}' AND Transaction_type = '{in_trans_typ}';")
        in_tr_anly_tab_qry_rslt = mycursor.fetchall()
        df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt), columns=['State','Transaction_count','Transaction_amount'])
        df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt)+1)))

#         # Total Transaction Amount table query
        mycursor.execute(f"SELECT SUM(Transaction_amt), AVG(Transaction_amt) FROM AGGREGATED_TRANSACTION WHERE Year = '{in_trans_yr}' AND Quater = '{in_trans_qtr}' AND Transaction_type = '{in_trans_typ}';")
        in_tr_am_qry_rslt = mycursor.fetchall()
        df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total','Average'])
        df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])
        
        # Total Transaction Count table query
        mycursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM AGGREGATED_TRANSACTION WHERE Year = '{in_trans_yr}' AND Quater = '{in_trans_qtr}' AND Transaction_type = '{in_trans_typ}';")
        in_tr_co_qry_rslt = mycursor.fetchall()
        df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total','Average'])
        df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])
# ----------------------   OUTPUT --------------------------------
#         ------  Geo visualization dashboard for Transaction ---- #
        # Drop a State column from df_in_tr_tab_qry_rslt
        df_trns_tab_qry_rslt.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        # Create a DataFrame with the state names column
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        # Combine the Gio State name with df_in_tr_tab_qry_rslt
        df_state_names_tra['Transaction_amount']=df_trns_tab_qry_rslt 
        # convert dataframe to csv file
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        # Read csv
        df_transaction = pd.read_csv('State_trans.csv')
        # Geo plot
        fig_transaction = px.choropleth(
            df_transaction,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='thermal',title = 'Transaction Map Analysis')
        fig_transaction.update_geos(fitbounds="locations", visible=False)
        fig_transaction.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_transaction,use_container_width=True)

        # ---------  All India Transaction Analysis Bar chart ----- #
        df_trns_tab_qry_rslt1 ['State'] = df_trns_tab_qry_rslt1['State'].astype(str)
        df_trns_tab_qry_rslt1 ['Transaction_amount'] = df_trns_tab_qry_rslt1['Transaction_amount'].astype(float)
        df_in_tr_tab_qry_rslt1_fig = px.bar(df_trns_tab_qry_rslt1, x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 700,)
        df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_in_tr_tab_qry_rslt1_fig,use_container_width=True)

#         # -------All India Total Transaction calculation Table ----  #
        st.header(':violet[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Table')
            st.dataframe(df_in_tr_anly_tab_qry_rslt1)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_in_tr_am_qry_rslt1)
            st.subheader('Transaction Count')
            st.dataframe(df_in_tr_co_qry_rslt1)


#     # -----------------------All India User -------------------------- #
        with tab2:
        
            col1, col2 = st.columns(2)
            with col1:
                in_user_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_user_yr')
            with col2:
                in_user_qtr = st.selectbox('**Select Quater**', ('1','2','3','4'),key='in_user_qtr')
        
#         # SQL Query

        # User Analysis Bar chart query
        mycursor.execute(f"SELECT State, SUM(UserCount) FROM AGGREGATED_USER WHERE Year =  '{in_user_yr}' AND Quater = '{in_user_qtr}' GROUP BY State;")
        in_user_tab_qry_rslt = mycursor.fetchall()
        df_in_user_tab_qry_rslt = pd.DataFrame(np.array(in_user_tab_qry_rslt), columns=['State', 'User Count'])
        df_in_user_tab_qry_rslt1 = df_in_user_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_user_tab_qry_rslt)+1)))

#         # Total User Count table query
        mycursor.execute(f"SELECT SUM(UserCount), AVG(UserCount) FROM AGGREGATED_USER WHERE Year = '{in_user_yr}' AND Quater = '{in_user_qtr}';")
        in_us_count_qry_rslt = mycursor.fetchall()
        df_in_us_count_qry_rslt = pd.DataFrame(np.array(in_us_count_qry_rslt), columns=['Total','Average'])
        df_in_us_count_qry_rslt1 = df_in_us_count_qry_rslt.set_index(['Average'])

        # ------ Output ------ #

        # ------    /  Geo visualization dashboard for User  /   ---- #
        # Drop a State column from df_in_us_tab_qry_rslt
        df_in_user_tab_qry_rslt.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data2 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        # Create a DataFrame with the state names column
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        # Combine the Gio State name with df_in_tr_tab_qry_rslt
        df_state_names_use['User Count']=df_in_user_tab_qry_rslt
        # convert dataframe to csv file
        df_state_names_use.to_csv('State_user.csv', index=False)
        # Read csv
        df_use = pd.read_csv('State_user.csv')
        # Geo plot
        fig_use = px.choropleth(
            df_use,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='User Count',color_continuous_scale='thermal',title = 'User Map Analysis')
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_use,use_container_width=True)

        # ----   /   All India User Analysis Bar chart   /     -------- #
        df_in_user_tab_qry_rslt1['State'] = df_in_user_tab_qry_rslt1['State'].astype(str)
        df_in_user_tab_qry_rslt1['User Count'] = df_in_user_tab_qry_rslt1['User Count'].astype(int)
        df_in_us_tab_qry_rslt1_fig = px.bar(df_in_user_tab_qry_rslt1 , x = 'State', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 700,)
        df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_in_us_tab_qry_rslt1_fig,use_container_width=True)

        # -----   /   All India Total User calculation Table   /   ----- #
        st.header(':violet[Total calculation]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_in_user_tab_qry_rslt1)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_in_us_count_qry_rslt1)



# -----------/     State wise       /----------------- #
    if option =='State wise':
        tab3, tab4 = st.tabs(['Transaction','User'])

    # --------/State wise Transaction/---------- # 
        with tab3:
            col1, col2,col3 = st.columns(3)
            with col1:
                st_tr_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_tr_st')
            with col2:
                st_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_tr_yr')
            with col3:
                st_tr_qtr = st.selectbox('**Select Quater**', ('1','2','3','4'),key='st_tr_qtr')
        
#         # SQL Query

        # Transaction Analysis bar chart query
        mycursor.execute(f"SELECT Transaction_type, Transaction_amt FROM AGGREGATED_TRANSACTION WHERE State =  '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quater = '{st_tr_qtr}';")
        st_tr_tab_bar_qry_rslt = mycursor.fetchall()
        df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt), columns=['Transaction_type', 'Transaction_amount'])
        df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt)+1)))

        # Transaction Analysis table query
        mycursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amt FROM AGGREGATED_TRANSACTION WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quater = '{st_tr_qtr}';")
        st_tr_anly_tab_qry_rslt = mycursor.fetchall()
        df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt), columns=['Transaction_type','Transaction_count','Transaction_amount'])
        df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt)+1)))

        # Total Transaction Amount table query
        mycursor.execute(f"SELECT SUM(Transaction_amt), AVG(Transaction_amt) FROM AGGREGATED_TRANSACTION WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quater = '{st_tr_qtr}';")
        st_tr_am_qry_rslt = mycursor.fetchall()
        df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Total','Average'])
        df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])
        
        # Total Transaction Count table query
        mycursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM AGGREGATED_TRANSACTION WHERE State =  '{st_tr_st}' AND Year ='{st_tr_yr}' AND Quater = '{st_tr_qtr}';")
        st_tr_co_qry_rslt = mycursor.fetchall()
        df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Total','Average'])
        df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])

# -----    /   State wise Transaction Analysis bar chart   /   ------ #
        df_st_tr_tab_bar_qry_rslt1['Transaction_type'] = df_st_tr_tab_bar_qry_rslt1['Transaction_type'].astype(str)
        df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(float)
        df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1 , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 500,)
        df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig,use_container_width=True)

        # ------  /  State wise Total Transaction calculation Table  /  ---- #
        st.header(':violet[Total calculation]')
        
        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_st_tr_anly_tab_qry_rslt1)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_st_tr_am_qry_rslt1)
            st.subheader('Transaction Count')
            st.dataframe(df_st_tr_co_qry_rslt1)


    # -------------/ State wise User/--------------- # 
        with tab4:
        
            col5, col6 = st.columns(2)
            with col5:
                st_us_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_us_st')
            with col6:
                st_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_us_yr')
        
        # SQL Query

        # User Analysis Bar chart query
        mycursor.execute(f"SELECT Quater, SUM(UserCount) FROM AGGREGATED_USER WHERE State = '{st_us_st}' AND Year = '{st_us_yr}' GROUP BY Quater;")
        st_us_tab_qry_rslt = mycursor.fetchall()
        df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['Quarter', 'User Count'])
        df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt)+1)))

        # Total User Count table query
        mycursor.execute(f"SELECT SUM(UserCount), AVG(UserCount) FROM AGGREGATED_USER WHERE State = '{st_us_st}' AND Year = '{st_us_yr}';")
        st_us_co_qry_rslt = mycursor.fetchall()
        df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['Total','Average'])
        df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['Average'])


        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_st_us_tab_qry_rslt1['Quarter'] = df_st_us_tab_qry_rslt1['Quarter'].astype(int)
        df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
        df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1 , x = 'Quarter', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 500,)
        df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_st_us_tab_qry_rslt1_fig,use_container_width=True)

        # ------    /   State wise User Total User calculation Table   /   -----#
        st.header(':violet[Total calculation]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_st_us_tab_qry_rslt1)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_st_us_co_qry_rslt1)



# # =================Top Transaction==================== #
    else:
        tab5, tab6 = st.tabs(['Transaction','User'])

    # --------------All India Top Transaction-------------- #
        with tab5:
            top_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_tr_yr')

        # SQL Query

        # Top Transaction Analysis bar chart query
        mycursor.execute(f"SELECT State, SUM(metric_amount) As Transaction_amount FROM TOP_TRANSACTION_DISTRICTS WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY metric_amount DESC LIMIT 10;")
        top_tr_tab_qry_rslt = mycursor.fetchall()
        df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt), columns=['State', 'Top Transaction amount'])
        df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_tab_qry_rslt)+1)))

        # Top Transaction Analysis table query
        mycursor.execute(f"SELECT State, SUM(metric_amount) as Transaction_amount, SUM(metric_count) as Transaction_count FROM TOP_TRANSACTION_DISTRICTS WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY metric_amount DESC LIMIT 10;")
        top_tr_anly_tab_qry_rslt = mycursor.fetchall()
        df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt), columns=['State', 'Top Transaction amount','Total Transaction count'])
        df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt)+1)))

        # -----   /   All India Top Transaction Analysis Bar chart   /   ----- #
        df_top_tr_tab_qry_rslt1['State'] = df_top_tr_tab_qry_rslt1['State'].astype(str)
        df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1['Top Transaction amount'].astype(float)
        df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1 , x = 'State', y ='Top Transaction amount', color ='Top Transaction amount', color_continuous_scale = 'thermal', title = 'Top Transaction Analysis Chart', height = 600,)
        df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_top_tr_tab_qry_rslt1_fig,use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Top Transaction Analysis')
        st.dataframe(df_top_tr_anly_tab_qry_rslt1)


# -------------------------       /     All India Top User        /        ------------------ #
        with tab6:
            top_user_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_user_yr')

        # SQL Query

        # Top User Analysis bar chart query
        mycursor.execute(f"SELECT State, SUM(RegisteredUsers) AS TOP_USER FROM TOP_USER_DISTRICTS WHERE Year= '{top_tr_yr}' GROUP BY State ORDER BY RegisteredUsers DESC LIMIT 10;")
        top_us_tab_qry_rslt = mycursor.fetchall()
        df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['State', 'Total User count'])
        df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_us_tab_qry_rslt)+1)))

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_top_us_tab_qry_rslt1['State'] = df_top_us_tab_qry_rslt1['State'].astype(str)
        df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
        df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1 , x = 'State', y ='Total User count', color ='Total User count', color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 600,)
        df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_top_us_tab_qry_rslt1_fig,use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Total User Analysis')
        st.dataframe(df_top_us_tab_qry_rslt1)
    
  
        
        

    



     






    

