import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

def analytics_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))
    
    if st.button("Get Analytics"):
        payload = {
            "start_date" : start_date.strftime("%Y-%m-%d"),
            "end_date" : end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics", json = payload)
        response = response.json()

        data = {
            "Category" : list(response.keys()),
            "Total" : [round(response[category]["total"],2) for category in response],
            "Percentage" : [round(response[category]["percentage"],2) for category in response],
        }

        df = pd.DataFrame(data)
        total_amount = df["Total"].sum()
        
        st.subheader("Expense Breakdown by Category")
        st.bar_chart(data = df.set_index("Category")["Total"], width = 0, height = 0, use_container_width = True)
        
        pie_chart = px.pie(
            df,
            names = "Category",
            values = "Total",
            color = "Category",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(pie_chart, use_container_width = True)

        st.write(df)
        st.write(f"**Total Amount:** {total_amount:.2f}")