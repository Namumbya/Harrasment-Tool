import streamlit as st
from utils.database import add_report
from datetime import datetime

def show():
    # Check if user is logged in
    if 'user_id' not in st.session_state or not st.session_state.user_id:
        st.warning("Please log in to submit a report")
        st.info("Use the navigation menu to go to the login page")
        return

    st.title("Report an Incident")
    
    with st.form("report_form"):
        incident_type = st.selectbox(
            "Type of Incident",
            ["Verbal Harassment", "Physical Harassment", "Online Harassment", 
             "Workplace Harassment", "Other"]
        )
        
        description = st.text_area(
            "Description",
            placeholder="Please provide details of the incident..."
        )
        
        location = st.text_input(
            "Location",
            placeholder="Where did this happen?"
        )
        
        submit = st.form_submit_button("Submit Report")
        
        if submit:
            if not all([incident_type, description, location]):
                st.error("Please fill in all fields")
            else:
                try:
                    report_id = add_report(
                        st.session_state.user_id,
                        incident_type,
                        description,
                        location
                    )
                    st.success("Report submitted successfully!")
                    st.info(f"Your report ID is: #{report_id}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
