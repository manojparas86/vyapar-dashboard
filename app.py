import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Vyapar Analytics Dashboard", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DUMMY DATA SETUP ---
# Real project mein ye data Database (SQL) se aayega
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Date': pd.to_datetime(['2026-04-01', '2026-04-02', '2026-04-03']),
        'Product': ['Mobile', 'Laptop', 'Headphones'],
        'Category': ['Electronics', 'Electronics', 'Accessories'],
        'Sales': [15000, 45000, 2000],
        'Profit': [1200, 3500, 400],
        'Stock': [10, 5, 25]
    })

# --- SIDEBAR: INPUT DATA ---
st.sidebar.header("📋 Data Entry")
with st.sidebar.form("entry_form"):
    new_date = st.date_input("Date", datetime.now())
    new_prod = st.text_input("Product Name")
    new_cat = st.selectbox("Category", ["Electronics", "FMCG", "Accessories", "Services"])
    new_sales = st.number_input("Sales Amount (₹)", min_value=0)
    new_profit = st.number_input("Profit (₹)", min_value=0)
    new_stock = st.number_input("Stock Update", min_value=0)
    
    submit = st.form_submit_button("Add Record")
    
    if submit:
        new_row = {
            'Date': pd.to_datetime(new_date),
            'Product': new_prod,
            'Category': new_cat,
            'Sales': new_sales,
            'Profit': new_profit,
            'Stock': new_stock
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Record Added!")

# --- MAIN DASHBOARD ---
st.title("📈 Vyapar Analytics Smart Dashboard")
st.write("Apne business ki progress track karein.")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
total_sales = st.session_state.data['Sales'].sum()
total_profit = st.session_state.data['Profit'].sum()
low_stock = st.session_state.data[st.session_state.data['Stock'] < 5].shape[0]

col1.metric("Total Sales", f"₹{total_sales:,}")
col2.metric("Total Profit", f"₹{total_profit:,}")
col3.metric("Profit Margin", f"{(total_profit/total_sales*100):.1f}%")
col4.metric("Low Stock Items", low_stock, delta_color="inverse")

st.divider()

# Charts Section
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sales Trend")
    fig_line = px.line(st.session_state.data, x='Date', y='Sales', markers=True, template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("Profit by Category")
    fig_pie = px.pie(st.session_state.data, values='Profit', names='Category', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Data Table
st.subheader("Recent Transactions")
st.dataframe(st.session_state.data.sort_values(by='Date', ascending=False), use_container_width=True)

# Download Report
csv = st.session_state.data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Full Report (CSV)", data=csv, file_name="business_report.csv", mime="text/csv")