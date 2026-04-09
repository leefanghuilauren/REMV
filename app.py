import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="MOE Bus Manager", layout="wide")

# --- INITIALIZE MOCK DATABASE (Session State) ---
if "orders" not in st.session_state:
    st.session_state.orders = []

# --- HELPER FUNCTIONS ---
def add_order(school, seats, pickup, dropoff, date, time):
    order_id = f"ORD-{len(st.session_state.orders) + 100}"
    st.session_state.orders.append({
        "ID": order_id,
        "School": school,
        "Seats": seats,
        "Route": f"{pickup} to {dropoff}",
        "Datetime": f"{date} {time}",
        "Status": "Pending Vendor Confirmation",
        "Driver": "Unassigned",
        "Vehicle": "Unassigned"
    })
    return order_id

# --- MAIN APP UI ---
st.title("🚌 MOE Bus Order Management")
st.markdown("Streamlining school transport with negotiated vendors.")

# Create the 5 main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 1. Place Order", 
    "⚙️ 2. Dispatch (Vendor)", 
    "📍 3. Teacher View", 
    "📊 4. Billing & Ratings",
    "👑 5. System Admin"
])
])

# --- TAB 1: SCHOOL PLACES ORDER ---
with tab1:
    st.header("Request New Bus Service")
    st.info("Pricing is automatically calculated based on pre-negotiated Master Contracts.")
    
    with st.form("order_form"):
        col1, col2 = st.columns(2)
        with col1:
            school_name = st.selectbox("School", ["MOE Secondary School", "MOE Primary School High", "Sembawang Secondary School"])
            seat_count = st.number_input("Number of Seats Required", min_value=10, max_value=80, value=40)
            date = st.date_input("Date of Trip", datetime.date.today())
        with col2:
            time = st.time_input("Pickup Time", datetime.time(9, 0))
            pickup_loc = st.text_input("Pickup Location", "MOE HQ")
            dropoff_loc = st.text_input("Destination", "Singapore Science Museum")
        
        submit = st.form_submit_button("Submit & Notify Vendor", type="primary")
        
        if submit:
            add_order(school_name, seat_count, pickup_loc, dropoff_loc, date, time)
            st.success("Order submitted! An automated email has been sent to the designated vendor.")

# --- TAB 2: VENDOR DISPATCH WORKFLOW ---
with tab2:
    st.header("Vendor Dispatch Dashboard")
    st.write("Manage incoming requests and assign vehicles.")
    
    if not st.session_state.orders:
        st.write("No active orders.")
    else:
        for i, order in enumerate(st.session_state.orders):
            with st.expander(f"Order {order['ID']} - {order['School']} ({order['Status']})", expanded=True):
                colA, colB = st.columns([2, 1])
                with colA:
                    st.write(f"**Route:** {order['Route']} | **Time:** {order['Datetime']} | **Seats:** {order['Seats']}")
                    
                with colB:
                    if order['Status'] == "Pending Vendor Confirmation":
                        if st.button("Accept & Assign", key=f"acc_{i}"):
                            st.session_state.orders[i]['Status'] = "Accepted"
                            st.session_state.orders[i]['Driver'] = "John D. (555-0199)"
                            st.session_state.orders[i]['Vehicle'] = "BUS-567"
                            st.rerun()
                        if st.button("Decline (Open to Pool)", key=f"dec_{i}"):
                            st.session_state.orders[i]['Status'] = "Open to Alternative Vendors"
                            st.rerun()
                    else:
                        st.write(f"**Assigned Driver:** {order['Driver']}")
                        st.write(f"**Vehicle:** {order['Vehicle']}")

# --- TAB 3: TEACHER EVENT DAY VIEW ---
with tab3:
    st.header("Today's Trips (Teacher View)")
    
    accepted_orders = [o for o in st.session_state.orders if o['Status'] == "Accepted"]
    
    if not accepted_orders:
        st.info("No confirmed trips for today yet. Go to Tab 1 to create one, and Tab 2 to accept it.")
    else:
        for order in accepted_orders:
            st.subheader(f"{order['Route']}")
            st.markdown(f"**Driver:** {order['Driver']} | **Vehicle:** {order['Vehicle']} | **ETA:** 15 mins")
            
            # Simple UI mockup for geolocation
            st.progress(65, text="Bus is en route. 65% to destination.")
            
            if st.button(f"Mark Trip as Completed", key=f"comp_{order['ID']}"):
                for i, o in enumerate(st.session_state.orders):
                    if o['ID'] == order['ID']:
                        st.session_state.orders[i]['Status'] = "Completed"
                st.success("Trip logged as complete. Please leave a rating in the Billing tab.")
                st.rerun()

# --- TAB 4: RECONCILIATION & RATINGS ---
with tab4:
    st.header("Post-Trip Management")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Provide Feedback")
        completed_orders = [o for o in st.session_state.orders if o['Status'] == "Completed"]
        
        if completed_orders:
            to_rate = st.selectbox("Select Trip to Rate", [o['ID'] for o in completed_orders])
            rating = st.slider("Service Rating", 1, 5, 5)
            feedback = st.text_area("Comments (Optional)")
            if st.button("Submit Feedback"):
                st.success("Feedback saved! This acts as your goods receipt.")
        else:
            st.write("Complete a trip in Tab 3 to leave a rating.")
            
    with col2:
        st.subheader("Monthly Reconciliation")
        st.write("App Data vs. Vendor Invoice (Mockup)")
        
        # Display mock dataframe
        df = pd.DataFrame(st.session_state.orders)
        if not df.empty:
            df = df[['ID', 'School', 'Status']]
            df['Contract Price'] = "$150.00" # Mock price
            st.dataframe(df, use_container_width=True)
            st.metric(label="Total to Authorize", value=f"${len(df) * 150}.00")

# --- TAB 5: SYSTEM ADMIN VIEW ---
with tab5:
    st.header("Master System Overview")
    st.write("Complete visibility into all cross-platform activity.")
    
    if not st.session_state.orders:
        st.info("No system activity logged yet.")
    else:
        # Convert session state to a Pandas DataFrame for easy data manipulation
        df_admin = pd.DataFrame(st.session_state.orders)
        
        # --- TOP LEVEL METRICS ---
        total_orders = len(df_admin)
        completed = len(df_admin[df_admin['Status'] == 'Completed'])
        pending = len(df_admin[df_admin['Status'] == 'Pending Vendor Confirmation'])
        escalated = len(df_admin[df_admin['Status'] == 'Open to Alternative Vendors'])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Trips Created", total_orders)
        col2.metric("Trips Completed", completed)
        col3.metric("Awaiting Vendor", pending)
        col4.metric("Escalated (Warning)", escalated, delta_color="inverse")
        
        st.divider()
        
        # --- MASTER DATABASE VIEW ---
        st.subheader("Master Order Database")
        
        # Add a filter so the admin can search by status
        all_statuses = df_admin['Status'].unique()
        status_filter = st.multiselect("Filter by Status", all_statuses, default=all_statuses)
        
        # Display the filtered table
        filtered_df = df_admin[df_admin['Status'].isin(status_filter)]
        st.dataframe(filtered_df, use_container_width=True)
        
        # Developer tool to clear the database while testing
        st.divider()
        if st.button("🚨 Clear All System Data (Dev Use Only)", type="secondary"):
            st.session_state.orders = []
            st.rerun()
