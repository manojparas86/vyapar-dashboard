import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIG & SEO ---
st.set_page_config(page_title="Vyapar Smart Pro", page_icon="💼", layout="wide")

# --- 2. DATA STORAGE ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])

# --- 3. ADVANCED UI (Background Image & Professional Styling) ---
st.markdown("""
    <style>
    /* Global Background Image with Glassmorphism Effect */
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
                    url("https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9);
    }

    /* Professional Card Styling */
    .section-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Metric Box for Million Dollar Look */
    .metric-box {
        background: #1e293b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .ad-banner {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("💼 Vyapar Menu")
# Home or Dashboard/Analysis structure
main_nav = st.sidebar.radio("Go To:", ["🏠 Home", "📊 Dashboard/Analysis"])

# Sub-menu only if Dashboard/Analysis is selected
sub_nav = None
if main_nav == "📊 Dashboard/Analysis":
    sub_nav = st.sidebar.selectbox("Choose Mode:", ["Dashboard (Entry)", "Analysis (Reporting)"])

# --- 5. SHARED LOGIC: METRICS CALCULATOR ---
def show_top_metrics():
    if not st.session_state.data.empty:
        df = st.session_state.data
        total_sales = df[df['Type'] == "Sell (Maal Becha)"]['Total'].sum()
        total_inv = df[df['Type'] == "Buy (Maal Khareeda)"]['Total'].sum()
        net_profit = total_sales - total_inv
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-box"><h4>Total Sales</h4><h2>₹{total_sales:,.2f}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><h4>Total Investment</h4><h2>₹{total_inv:,.2f}</h2></div>', unsafe_allow_html=True)
        with m3:
            color = "#4ade80" if net_profit >= 0 else "#f87171"
            st.markdown(f'<div class="metric-box"><h4>Net Profit/Loss</h4><h2 style="color:{color}">₹{net_profit:,.2f}</h2></div>', unsafe_allow_html=True)
        st.write("")
    else:
        st.warning("Pehle Dashboard mein entry karein taaki metrics calculate ho sakein.")

# --- 6. PAGE LOGIC ---

if main_nav == "🏠 Home":
    st.markdown('<div style="background: rgba(15,23,42,0.85); color:white; padding:3rem; border-radius:20px; text-align:center;">'
                '<h1>Apne Business ko Smart Banayein 🚀</h1><p>High Performance Professional Business Suite</p></div>', unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-card"><h3>🔍 Inventory Search Tool</h3>', unsafe_allow_html=True)
        search = st.text_input("Product name likhein search karne ke liye...")
        if search and not st.session_state.data.empty:
            res = st.session_state.data[st.session_state.data['Product'].str.contains(search, case=False)]
            st.dataframe(res)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card"><h3>👤 About Me</h3><p>Main ek expert developer hoon aur ye Vyapar Pro ka advanced version hai jo 2026 ki tech par based hai.</p></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ad-banner">🔥 OFFER: Get 1TB Cloud Storage Free with Pro!</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="section-card"><h3>📞 Contact Us</h3><p>Support: +91-RONIT-PRO<br>Email: ronit@vyaparpro.com</p></div>', unsafe_allow_html=True)
        
        with st.expander("❓ Product Query"):
            with st.form("pq"):
                st.text_input("Product Name")
                st.text_area("Your Question")
                st.form_submit_button("Send")

elif sub_nav == "Dashboard (Entry)":
    st.title("💼 Vyapar Smart Dashboard")
    show_top_metrics()
    
    with st.expander("➕ Nayi Transaction Entry", expanded=True):
        c1, c2, c3 = st.columns(3)
        d_date = c1.date_input("Date", datetime.now())
        d_type = c2.selectbox("Action", ["Buy (Maal Khareeda)", "Sell (Maal Becha)"])
        d_name = c3.text_input("Product Name")
        
        c4, c5 = st.columns(2)
        d_qty = c4.number_input("Quantity", min_value=0)
        d_price = c5.number_input("Price (₹)", min_value=0.0)
        
        if st.button("Save Entry 💾", use_container_width=True):
            # Error Message Box Handling
            if not d_name:
                st.error("🚨 ERROR: Product ka naam likhna zaroori hai!")
            elif d_qty <= 0 or d_price <= 0:
                st.error("🚨 ERROR: Quantity aur Price zero nahi ho sakte!")
            else:
                total = d_qty * d_price
                new_row = pd.DataFrame([[d_date, d_type, d_name, d_qty, d_price, total]], 
                                       columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                st.success(f"Dabaake entry hui: {d_name} saved!")

    st.subheader("📋 Pichli Sabhi Entries")
    st.dataframe(st.session_state.data.sort_values(by="Date", ascending=False), use_container_width=True)

elif sub_nav == "Analysis (Reporting)":
    st.title("📈 Business Analysis")
    show_top_metrics()
    
    if not st.session_state.data.empty:
        df = st.session_state.data.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        
        col_charts1, col_charts2 = st.columns(2)
        
        with col_charts1:
            st.subheader("📅 Date-wise Earning (Line Chart)")
            line_fig = px.line(df, x='Date', y='Total', color='Type', markers=True, title="Growth Over Time")
            st.plotly_chart(line_fig, use_container_width=True)
            
        with col_charts2:
            st.subheader("📊 Product wise Profit (Bar Chart)")
            bar_fig = px.bar(df, x='Product', y='Total', color='Type', barmode='group')
            st.plotly_chart(bar_fig, use_container_width=True)
    else:
        st.info("Analysis dekhne ke liye Dashboard mein data bharna shuru karein.")

# Footer
st.markdown(f"<br><hr><p style='text-align: center;'>Built with ❤️ by Ronit | 2026</p>", unsafe_allow_html=True)