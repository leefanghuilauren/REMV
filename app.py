import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="MOE Operations Portal", layout="wide", initial_sidebar_state="expanded")

# --- INITIALIZE MOCK DATABASES (Session State) ---
if "bus_orders" not in st.session_state:
    st.session_state.bus_orders = []
if "cca_bookings" not in st.session_state:
    st.session_state.cca_bookings = []
if "goods_orders" not in st.session_state:
    st.session_state.goods_orders = []
if "contracts" not in st.session_state:
    st.session_state.contracts = {"bus": False, "cca": False}

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏫 MOE Portal")
app_mode = st.sidebar.radio(
    "Select Module",
    ["🚌 Transport Services", "⚽ CCA Instructors", "📦 Goods & Services", "👑 Master Admin"]
)
st.sidebar.divider()
st.sidebar.info("Logged in as: School Admin")

# ==========================================
# MINI-APP 1: TRANSPORT SERVICES (BUS)
# ==========================================
if app_mode == "🚌 Transport Services":
    st.title("🚌 Transport Services Module")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Master Contract", "📝 Book Bus", "⚙️ Vendor Dispatch", "📊 Trip & Billing"])
    
    with tab1:
        st.header("Master Transport Contract")
        
        if st.session_state.contracts["bus"]:
            st.success("✅ Master Contract Active: 'City Transit Solutions' locked in.")
            if st.button("🗑️ Remove Contract (Reset)", key="reset_bus_con"):
                st.session_state.contracts["bus"] = False
                st.rerun()
        else:
            st.warning("No active contract for the current year. Please upload one.")
            if st.button("📥 Simulate Contract Upload", type="primary", key="sim_bus_upload"):
                st.session_state.contracts["bus"] = True
                st.rerun()

    with tab2:
        st.header("Request Bus Service")
        if not st.session_state.contracts["bus"]:
            st.error("🔒 Please upload a Master Contract in Tab 1 first to unlock booking.")
        else:
            with st.form("bus_form"):
                col1, col2 = st.columns(2)
                with col1:
                    seats = st.number_input("Seats Required", min_value=10, max_value=80, value=40)
                    date = st.date_input("Date of Trip", datetime.date.today())
                with col2:
                    time = st.time_input("Pickup Time", datetime.time(9, 0))
                    pickup = st.text_input("Pickup Location", "School Main Gate")
                    dropoff = st.text_input("Destination", "Science Centre")
                
                if st.form_submit_button("Submit Order to Contracted Vendor", type="primary"):
                    st.session_state.bus_orders.append({
                        "ID": f"BUS-{len(st.session_state.bus_orders)+100}",
                        "Route": f"{pickup} to {dropoff}",
                        "Date": str(date),
                        "Status": "Pending Vendor Assignment",
                        "Driver": "Unassigned"
                    })
                    st.success("Order dispatched directly to contracted vendor.")

    with tab3:
        st.header("Vendor Dashboard (Assigned Jobs)")
        for i, order in enumerate(st.session_state.bus_orders):
            if order["Status"] == "Pending Vendor Assignment":
                with st.expander(f"{order['ID']} -
