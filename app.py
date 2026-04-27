import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Operations Portal Prototype", layout="wide", initial_sidebar_state="expanded")

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
st.sidebar.title("🏫 Operations Portal")
st.sidebar.caption("Prototype Version 1.0")
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
    st.write("End-to-end management of ad-hoc school bus logistics.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Master Contract", "📝 Book Bus", "⚙️ Vendor Dispatch", "📊 Trip & Billing"])
    
    with tab1:
        st.header("Master Transport Contract")
        st.write("Upload the yearly awarded contract to lock in vendors and rates.")
        
        if st.session_state.contracts["bus"]:
            st.success("✅ Master Contract Active: 'City Transit Solutions' locked in at $150/trip.")
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
                        "Driver": "Unassigned",
                        "Base Rate": 150
                    })
                    st.success("Order dispatched directly to contracted vendor.")

    with tab3:
        st.header("Vendor Dashboard (Assigned Jobs)")
        st.write("Vendor accepts the mandated job and assigns driver details.")
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
            st.subheader("Active Trips (Ground Execution)")
            for i, order in enumerate(st.session_state.bus_orders):
                if order["Status"] == "Assigned":
                    with st.expander(f"🚌 Log Event: {order['ID']} - {order['Route']}", expanded=True):
                        st.info(f"Driver: {order['Driver']}")
                        
                        st.write("**Exception Handling & Feedback**")
                        late_charge = st.checkbox("⚠️ Late Bus Charge Applicable (-$50 penalty)", key=f"late_{i}")
                        size_mismatch = st.checkbox("⚠️ Bus Size Mismatch", key=f"size_{i}")
                        feedback = st.text_area("On-the-ground Feedback / Remarks", placeholder="e.g., Driver was 15 mins late...", key=f"fb_{i}")
                        
                        if st.button("Submit Log & Mark Completed", key=f"comp_bus_{i}", type="primary"):
                            st.session_state.bus_orders[i]["Status"] = "Completed"
                            st.session_state.bus_orders[i]["Late Charge"] = "Yes" if late_charge else "No"
                            st.session_state.bus_orders[i]["Size Mismatch"] = "Yes" if size_mismatch else "No"
                            st.session_state.bus_orders[i]["Feedback"] = feedback
                            # Calculate final dynamic cost
                            final_cost = 150 - (50 if late_charge else 0)
                            st.session_state.bus_orders[i]["Final Cost"] = final_cost
                            st.rerun()
                            
        with col2:
            st.subheader("Billing Verification")
            df_bus = pd.DataFrame([o for o in st.session_state.bus_orders if o["Status"] == "Completed"])
            if not df_bus.empty:
                st.dataframe(df_bus[['ID', 'Date', 'Late Charge', 'Feedback', 'Final Cost']], use_container_width=True)
                st.metric("Total Payable (Adjusted)", f"${df_bus['Final Cost'].sum():.2f}")

# ==========================================
# MINI-APP 2: CCA INSTRUCTORS
# ==========================================
elif app_mode == "⚽ CCA Instructors":
    st.title("⚽ CCA Instructor Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Master Contract", "📅 Book Session", "📋 Instructor Portal", "💰 Invoice & Verify"])
    
    with tab1:
        st.header("Master CCA Contract")
        if st.session_state.contracts["cca"]:
            st.success("✅ Master Contract Active: 'Elite Sports Academy' locked in at $80/hr.")
            if st.button("🗑️ Remove Contract (Reset)", key="reset_cca_con"):
                st.session_state.contracts["cca"] = False
                st.rerun()
        else:
            st.warning("No active contract. Please upload one.")
            if st.button("📥 Simulate Contract Upload", type="primary", key="sim_cca_upload"):
                st.session_state.contracts["cca"] = True
                st.rerun()

    with tab2:
        st.header("Book CCA Sessions")
        if not st.session_state.contracts["cca"]:
            st.error("🔒 Please upload a Master Contract in Tab 1 first to unlock booking.")
        else:
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
                        st.session_state.cca_bookings[i]["Final Cost"] = sess['Hours'] * 80
                        st.rerun()

    with tab4:
        st.header("End of Month Invoice Generation")
        df_cca = pd.DataFrame([s for s in st.session_state.cca_bookings if s["Status"] == "Completed"])
        if not df_cca.empty:
            st.dataframe(df_cca[['ID', 'Group', 'Date', 'Hours', 'Attendance', 'Final Cost']], use_container_width=True)
            st.metric("Total Consolidated Invoice", f"${df_cca['Final Cost'].sum():.2f}")
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
                        receipt_file = st.file_uploader("📎 Attach Delivery Order / Photo Evidence", type=["pdf", "png", "jpg"], key=f"file_{i}")
                    
                    with colB:
                        remarks = st.text_area("Discrepancy Remarks", placeholder="Missing items, damaged goods, etc.", key=f"g_rem_{i}")
                        
                        if st.button("Acknowledge Receipt & Verify for Payment", key=f"rec_{i}", type="primary"):
                            st.session_state.goods_orders[i]["Status"] = "Completed & Verified"
                            st.session_state.goods_orders[i]["Rating"] = f"{rating} Stars"
                            st.session_state.goods_orders[i]["Artifact Attached"] = "Yes" if receipt_file else "No"
                            st.session_state.goods_orders[i]["Remarks"] = remarks
                            st.rerun()
        
        st.subheader("Verified Payments Pipeline")
        df_goods = pd.DataFrame([g for g in st.session_state.goods_orders if g["Status"] == "Completed & Verified"])
        if not df_goods.empty:
            st.dataframe(df_goods[['ID', 'Vendor', 'Amount', 'Artifact Attached', 'Remarks']], use_container_width=True)

# ==========================================
# MASTER ADMIN DASHBOARD
# ==========================================
elif app_mode == "👑 Master Admin":
    st.title("👑 System Admin: Master Overview")
    
    admin_password = st.text_input("Enter Admin Password (Try '1234'):", type="password")
    
    if admin_password == "1234":
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transport Trips", len(st.session_state.bus_orders))
        col2.metric("Total CCA Sessions", len(st.session_state.cca_bookings))
        col3.metric("Total Goods POs", len(st.session_state.goods_orders))
        
        st.divider()
        st.subheader("Raw Data Exports")
        
        tabA, tabB, tabC = st.tabs(["Bus Data", "CCA Data", "Goods Data"])
        
        with tabA: 
            st.dataframe(pd.DataFrame(st.session_state.bus_orders), use_container_width=True)
            st.write("---") 
            if st.session_state.bus_orders:
                df_export = pd.DataFrame(st.session_state.bus_orders)
                csv_data = df_export.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download Bus Bookings (CSV)", data=csv_data, file_name="moe_bus_bookings.csv", mime="text/csv", type="primary")
            else:
                st.info("No bus bookings available to download yet.")
        
        with tabB: 
            st.dataframe(pd.DataFrame(st.session_state.cca_bookings), use_container_width=True)
            st.write("---")
            if st.session_state.cca_bookings:
                df_export_cca = pd.DataFrame(st.session_state.cca_bookings)
                csv_data_cca = df_export_cca.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download CCA Bookings (CSV)", data=csv_data_cca, file_name="moe_cca_bookings.csv", mime="text/csv", type="primary")

        with tabC: 
            st.dataframe(pd.DataFrame(st.session_state.goods_orders), use_container_width=True)
            st.write("---")
            if st.session_state.goods_orders:
                df_export_goods = pd.DataFrame(st.session_state.goods_orders)
                csv_data_goods = df_export_goods.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download Goods Orders (CSV)", data=csv_data_goods, file_name="moe_goods_orders.csv", mime="text/csv", type="primary")
        
        st.divider()
        if st.button("🚨 Clear All System Data (Reset Prototype)", type="secondary"):
            st.session_state.bus_orders = []
            st.session_state.cca_bookings = []
            st.session_state.goods_orders = []
            st.session_state.contracts = {"bus": False, "cca": False}
            st.rerun()
            
    elif admin_password != "":
        st.error("Incorrect password.")
