import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import time

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Vyapar Smart Pro | Ronit Edition",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PERMANENT DATABASE ENGINE ---
DB_FILE = "data.csv"

def load_database():
    """Permanent storage se data load karne ke liye"""
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Date formatting to prevent Arrow/Pyarrow errors
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        except Exception:
            return pd.DataFrame(columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])
    return pd.DataFrame(columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])

def save_to_database(df):
    """Data ko permanent CSV file mein save karne ke liye"""
    df.to_csv(DB_FILE, index=False)

# Session State Initialize
if 'data' not in st.session_state:
    st.session_state.data = load_database()

# --- 3. CUSTOM CSS FOR MILLION DOLLAR LOOK ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                    url("https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Metrics Card */
    .metric-card {
        background: #1e293b;
        color: #f8fafc;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border-bottom: 5px solid #3b82f6;
    }
    
    /* Custom Section Cards */
    .content-section {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Professional Ad Banners */
    .ad-card {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .ad-gold {
        background: linear-gradient(135deg, #b45309, #f59e0b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
    }

    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SHARED UTILITIES ---
def get_metrics():
    df = st.session_state.data
    if not df.empty:
        sales = df[df['Type'] == "Sell (Maal Becha)"]['Total'].sum()
        investment = df[df['Type'] == "Buy (Maal Khareeda)"]['Total'].sum()
        profit = sales - investment
        return sales, investment, profit
    return 0.0, 0.0, 0.0

def display_metrics_ui():
    s, i, p = get_metrics()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><h4>💰 Total Revenue</h4><h2>₹{s:,.2f}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h4>📉 Total Investment</h4><h2>₹{i:,.2f}</h2></div>', unsafe_allow_html=True)
    with c3:
        color = "#22c55e" if p >= 0 else "#ef4444"
        st.markdown(f'<div class="metric-card"><h4>📈 Net Profit/Loss</h4><h2 style="color:{color}">₹{p:,.2f}</h2></div>', unsafe_allow_html=True)
    st.write("---")

unique_prods = sorted(st.session_state.data['Product'].unique().tolist()) if not st.session_state.data.empty else []

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2652/2652234.png", width=100)
    st.title("💼 Vyapar Pro v2.0")
    st.write("**Empowering Local Business**")
    st.markdown("---")
    
    # New Menu Structure as requested
    menu = st.radio("MAIN MENU", [
        "🏠 Home Dashboard", 
        "➕ New Transaction", 
        "📈 Business Analytics", 
        "🔍 History & Search", 
        "⚙️ Database Settings"
    ])
    
    st.markdown("---")
    st.info("💡 Tip: Use 'History' to find transactions older than 1 year.")

# --- 6. PAGE LOGIC ---

# PAGE 1: HOME DASHBOARD
if menu == "🏠 Home Dashboard":
    st.markdown('<div style="background: #0f172a; color:white; padding:40px; border-radius:20px; text-align:center; margin-bottom:20px;">'
                '<h1>Welcome to Vyapar Smart Pro 🚀</h1>'
                '<p>High Performance Professional Business Suite | Dev: Ronit</p></div>', unsafe_allow_html=True)
    
    display_metrics_ui()
    
    col_main, col_ads = st.columns([2, 1])
    
    with col_main:
        st.markdown('<div class="content-section"><h3>🔍 Fast Inventory Search</h3>', unsafe_allow_html=True)
        search_query = st.text_input("Product name likhein turant stock check karne ke liye...")
        if search_query and not st.session_state.data.empty:
            match = st.session_state.data[st.session_state.data['Product'].str.contains(search_query, case=False)].copy()
            if not match.empty:
                match['Date'] = match['Date'].astype(str)
                st.dataframe(match.tail(10), use_container_width=True)
            else:
                st.warning("Maal nahi mila! Please check the spelling.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-section"><h3>📞 Contact Us (Support)</h3>'
                    '<p><b>Business Name:</b> Vyapar Smart Pro Enterprise</p>'
                    '<p><b>Phone:</b> +91-91234-XXXXX (Ronit Support)</p>'
                    '<p><b>Email:</b> ronitparas@gmail.com</p>'
                    '<p><b>Website:</b> www.ronitvyaparpro.com</p></div>', unsafe_allow_html=True)

    with col_ads:
        st.markdown('<div class="ad-gold">🔥 LIMITED OFFER<br>Get 50% Off on Pro Cloud Sync!</div>', unsafe_allow_html=True)
        st.markdown('<div class="ad-card">📊 UPGRADE TO PRO<br>Advanced AI GST Invoicing & Tax Reports</div>', unsafe_allow_html=True)
        st.markdown('<div class="ad-card">📱 MOBILE APP<br>Download Vyapar Pro for Android & iOS</div>', unsafe_allow_html=True)
        st.markdown('<div class="ad-gold">🔒 SECURITY<br>100% Data Encryption Enabled</div>', unsafe_allow_html=True)
        st.markdown('<div class="ad-card">🏢 LOAN SERVICES<br>Quick Business Loans up to ₹50 Lakhs</div>', unsafe_allow_html=True)

# PAGE 2: NEW TRANSACTION
elif menu == "➕ New Transaction":
    st.title("➕ Nayi Entry (Sale/Purchase)")
    display_metrics_ui()
    
    with st.container():
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        with st.form("main_entry", clear_on_submit=True):
            f1, f2, f3 = st.columns(3)
            e_date = f1.date_input("Date", datetime.now())
            e_type = f2.selectbox("Action", ["Buy (Maal Khareeda)", "Sell (Maal Becha)"])
            
            is_old = f3.toggle("Purana Product?")
            if is_old and unique_prods:
                e_name = f3.selectbox("List se chunein", unique_prods)
            else:
                e_name = f3.text_input("Product ka Naam")
            
            f4, f5 = st.columns(2)
            e_qty = f4.number_input("Quantity (Nagma)", min_value=1)
            e_price = f5.number_input("Price per Unit (₹)", min_value=0.0)
            
            if st.form_submit_button("SAVE DATA PERMANENTLY 💾", use_container_width=True):
                if e_name:
                    total = e_qty * e_price
                    new_row = pd.DataFrame([[e_date, e_type, e_name.strip().capitalize(), e_qty, e_price, total]], 
                                           columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])
                    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                    save_to_database(st.session_state.data)
                    st.success(f"Entry Saved: {e_name} (₹{total})")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Galti: Product ka naam likhna zaroori hai!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📋 Last 5 Entries")
    if not st.session_state.data.empty:
        rdf = st.session_state.data.tail(5).copy()
        rdf['Date'] = rdf['Date'].astype(str)
        st.table(rdf)

# PAGE 3: BUSINESS ANALYTICS
elif menu == "📈 Business Analytics":
    st.title("📈 Advanced Business Intelligence")
    display_metrics_ui()
    
    if not st.session_state.data.empty:
        df_p = st.session_state.data.copy()
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            fig_l = px.line(df_p, x='Date', y='Total', color='Type', title="Monthly Progress", markers=True)
            st.plotly_chart(fig_l, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with g2:
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            fig_p = px.pie(df_p, values='Total', names='Product', title="Product Sales Share", hole=0.4)
            st.plotly_chart(fig_p, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        fig_b = px.bar(df_p, x='Date', y='Total', color='Product', barmode='group', title="Daily Breakdown")
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Data nahi mil raha analytics dikhane ke liye.")

# PAGE 4: HISTORY & SEARCH
elif menu == "🔍 History & Search":
    st.title("🔍 Transaction History Vault")
    
    if not st.session_state.data.empty:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns([3, 1])
        h_search = col_s1.text_input("Kisi bhi purani entry ko search karein...")
        h_filter = col_s2.multiselect("Filter", ["Buy (Maal Khareeda)", "Sell (Maal Becha)"], default=["Buy (Maal Khareeda)", "Sell (Maal Becha)"])
        
        f_df = st.session_state.data[st.session_state.data['Type'].isin(h_filter)]
        if h_search:
            f_df = f_df[f_df['Product'].str.contains(h_search, case=False)]
        
        final_df = f_df.sort_values(by='Date', ascending=False)
        final_df['Date'] = final_df['Date'].astype(str) # Error Fix
        
        st.dataframe(final_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Option
        csv = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Business Report (CSV)", csv, "vyapar_report.csv", "text/csv")
    else:
        st.warning("History is empty.")

# PAGE 5: DATABASE SETTINGS
elif menu == "⚙️ Database Settings":
    st.title("⚙️ System Management")
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.subheader("System Information")
    st.write(f"**Database Status:** Connected ✅")
    st.write(f"**Storage Path:** `{os.path.abspath(DB_FILE)}`")
    st.write(f"**Total Records:** {len(st.session_state.data)}")
    
    st.markdown("---")
    st.subheader("Danger Zone")
    st.error("Neeche diye gaye button se aapka saara data permanent delete ho jayega!")
    
    if st.button("🚨 Reset All Data"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.session_state.data = pd.DataFrame(columns=['Date', 'Type', 'Product', 'Qty', 'Price', 'Total'])
            st.success("Database has been reset! Refreshing...")
            time.sleep(1)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <hr>
    <div class="footer-text">
        <p><b>Vyapar Smart Pro v2.0</b> | Designed & Developed by <b>Ronit</b></p>
        <p>Support: ronitparas@gmail.com | 2026 Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)