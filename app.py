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
        st.write("Upload the yearly awarded contract to lock in vendors and rates.")
        uploaded_file = st.file_uploader("Upload Contract (PDF/Excel)", type=['pdf', 'xlsx'], key="bus_contract")
        if uploaded_file or st.session_state.contracts["bus"]:
            st.session_state.contracts["bus"] = True
            st.success("✅ Master Contract Active: 'City Transit Solutions' locked in at $150/trip.")
        else:
            st.warning("No active contract for the current year. Please upload one.")

    with tab2:
        st.header("Request Bus Service")
        if not st.session_state.contracts["bus"]:
            st.error("Please upload a Master Contract in Tab 1 first.")
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
        st.write("Vendor accepts the mandated job and assigns details.")
        for i, order in enumerate(st.session_state.bus_orders):
            if order["Status"] == "Pending Vendor Assignment":
                with st.expander(f"{order['ID']} - {order['Route']}"):
                    st.write(f"**Date:** {order['Date']}")
                    driver_name = st.text_input("Assign Driver Name", key=f"d_name_{i}")
                    veh_num = st.text_input("Assign Vehicle Number", key=f"v_num_{i}")
                    if st.button("Acknowledge & Assign", key=f"ack_bus_{i}"):
                        st.session_state.bus_orders[i]["Status"] = "Assigned"
                        st.session_state.bus_orders[i]["Driver"] = f"{driver_name} ({veh_num})"
                        st.rerun()

    with tab4:
        st.header("Event Day & Reconciliation")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Active Trips")
            for i, order in enumerate(st.session_state.bus_orders):
                if order["Status"] == "Assigned":
                    st.info(f"**{order['ID']}**: {order['Route']} | Driver: {order['Driver']}")
                    if st.button("Mark Completed", key=f"comp_bus_{i}"):
                        st.session_state.bus_orders[i]["Status"] = "Completed"
                        st.rerun()
        with col2:
            st.subheader("Billing Verification")
            df_bus = pd.DataFrame([o for o in st.session_state.bus_orders if o["Status"] == "Completed"])
            if not df_bus.empty:
                st.dataframe(df_bus[['ID', 'Route', 'Date']], use_container_width=True)
                st.metric("Total Payable", f"${len(df_bus) * 150}.00")

# ==========================================
# MINI-APP 2: CCA INSTRUCTORS
# ==========================================
elif app_mode == "⚽ CCA Instructors":
    st.title("⚽ CCA Instructor Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Master Contract", "📅 Book Session", "📋 Instructor Portal", "💰 Invoice & Verify"])
    
    with tab1:
        st.header("Master CCA Contract")
        uploaded_cca = st.file_uploader("Upload Contract (PDF/Excel)", type=['pdf', 'xlsx'], key="cca_contract")
        if uploaded_cca or st.session_state.contracts["cca"]:
            st.session_state.contracts["cca"] = True
            st.success("✅ Master Contract Active: 'Elite Sports Academy' locked in at $80/hr.")
        else:
            st.warning("No active contract. Please upload.")

    with tab2:
        st.header("Book CCA Sessions")
        if st.session_state.contracts["cca"]:
            with st.form("cca_form"):
                cca_group = st.selectbox("CCA Group", ["Football", "Basketball", "Robotics Club"])
                sess_date = st.date_input("Session Date", datetime.date.today())
                hours = st.number_input("Duration (Hours)", 1, 4, 2)
                if st.form_submit_button("Book Instructor", type="primary"):
                    st.session_state.cca_bookings.append({
                        "ID": f"CCA-{len(st.session_state.cca_bookings)+100}",
                        "Group": cca_group,
                        "Date": str(sess_date),
                        "Hours": hours,
                        "Status": "Pending Instructor Acceptance",
                        "Attendance": "Not Taken"
                    })
                    st.success("Session booked. Instructor notified.")

    with tab3:
        st.header("Instructor Portal")
        st.write("Instructors accept sessions and take attendance on the day.")
        for i, sess in enumerate(st.session_state.cca_bookings):
            with st.expander(f"{sess['ID']} - {sess['Group']} on {sess['Date']} ({sess['Status']})"):
                if sess["Status"] == "Pending Instructor Acceptance":
                    if st.button("Accept Session", key=f"acc_cca_{i}"):
                        st.session_state.cca_bookings[i]["Status"] = "Accepted"
                        st.rerun()
                elif sess["Status"] == "Accepted":
                    att_count = st.number_input("Students Present", 0, 50, 0, key=f"att_{i}")
                    if st.button("Submit Attendance & Mark Complete", key=f"comp_cca_{i}"):
                        st.session_state.cca_bookings[i]["Attendance"] = f"{att_count} students"
                        st.session_state.cca_bookings[i]["Status"] = "Completed"
                        st.rerun()

    with tab4:
        st.header("End of Month Invoice Generation")
        df_cca = pd.DataFrame([s for s in st.session_state.cca_bookings if s["Status"] == "Completed"])
        if not df_cca.empty:
            df_cca['Cost'] = df_cca['Hours'] * 80
            st.dataframe(df_cca[['ID', 'Group', 'Date', 'Hours', 'Attendance', 'Cost']], use_container_width=True)
            st.metric("Total Consolidated Invoice", f"${df_cca['Cost'].sum():.2f}")
            if st.button("Verify & Authorize Payment", type="primary"):
                st.success("Payment Authorized and routed to Finance.")
        else:
            st.write("No completed sessions to bill.")

# ==========================================
# MINI-APP 3: GOODS & SERVICES
# ==========================================
elif app_mode == "📦 Goods & Services":
    st.title("📦 Goods & Services Receipt")
    
    tab1, tab2, tab3 = st.tabs(["🛒 Issue PO", "🚚 Supplier Dispatch", "📦 Goods Receipt & Pay"])
    
    with tab1:
        st.header("Issue Purchase Order")
        with st.form("po_form"):
            item_desc = st.text_input("Item/Service Description", "Science Lab Beakers (Pack of 50)")
            vendor = st.selectbox("Supplier", ["EduSupplies Ltd", "TechCorp SG", "OfficeWorld"])
            amount = st.number_input("PO Amount ($)", min_value=1.0, value=250.0)
            if st.form_submit_button("Issue Order", type="primary"):
                st.session_state.goods_orders.append({
                    "ID": f"PO-{len(st.session_state.goods_orders)+100}",
                    "Item": item_desc,
                    "Vendor": vendor,
                    "Amount": amount,
                    "Status": "Sent to Supplier",
                    "Rating": "None"
                })
                st.success("PO Issued to Supplier.")

    with tab2:
        st.header("Supplier Portal")
        for i, po in enumerate(st.session_state.goods_orders):
            if po["Status"] == "Sent to Supplier":
                with st.expander(f"{po['ID']} - {po['Item']}"):
                    st.write(f"**Amount:** ${po['Amount']}")
                    if st.button("Mark as Delivered / Service Rendered", key=f"del_po_{i}"):
                        st.session_state.goods_orders[i]["Status"] = "Delivered (Pending Receipt)"
                        st.rerun()

    with tab3:
        st.header("Goods Receipt & Verification")
        for i, po in enumerate(st.session_state.goods_orders):
            if po["Status"] == "Delivered (Pending Receipt)":
                with st.container(border=True):
                    st.write(f"**{po['ID']} | {po['Vendor']}** - {po['Item']}")
                    colA, colB = st.columns(2)
                    with colA:
                        rating = st.slider("Rate Quality", 1, 5, 5, key=f"rate_{i}")
                    with colB:
                        if st.button("Acknowledge Receipt & Verify for Payment", key=f"rec_{i}"):
                            st.session_state.goods_orders[i]["Status"] = "Completed & Verified"
                            st.session_state.goods_orders[i]["Rating"] = f"{rating} Stars"
                            st.rerun()
        
        st.subheader("Verified Payments Pipeline")
        df_goods = pd.DataFrame([g for g in st.session_state.goods_orders if g["Status"] == "Completed & Verified"])
        if not df_goods.empty:
            st.dataframe(df_goods[['ID', 'Vendor', 'Item', 'Amount', 'Rating']], use_container_width=True)

# ==========================================
# MASTER ADMIN DASHBOARD
# ==========================================
elif app_mode == "👑 Master Admin":
    st.title("👑 System Admin: Master Overview")
    
    admin_password = st.text_input("Enter Admin Password:", type="password")
    if admin_password == "EduTransit2026!":
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transport Trips", len(st.session_state.bus_orders))
        col2.metric("Total CCA Sessions", len(st.session_state.cca_bookings))
        col3.metric("Total Goods POs", len(st.session_state.goods_orders))
        
        st.divider()
        st.subheader("Raw Data Exports")
        
        tabA, tabB, tabC = st.tabs(["Bus Data", "CCA Data", "Goods Data"])
        with tabA: st.dataframe(pd.DataFrame(st.session_state.bus_orders), use_container_width=True)
        with tabB: st.dataframe(pd.DataFrame(st.session_state.cca_bookings), use_container_width=True)
        with tabC: st.dataframe(pd.DataFrame(st.session_state.goods_orders), use_container_width=True)
        
        st.divider()
        if st.button("🚨 Clear All System Data (Dev Use Only)", type="secondary"):
            st.session_state.bus_orders = []
            st.session_state.cca_bookings = []
            st.session_state.goods_orders = []
            st.session_state.contracts = {"bus": False, "cca": False}
            st.rerun()
    elif admin_password != "":
        st.error("Incorrect password.")
