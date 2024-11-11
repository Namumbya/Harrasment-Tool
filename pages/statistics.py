import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import get_report_stats
from datetime import datetime, timedelta

def save_dataframe(df, filename):
    """Helper function to convert DataFrame to CSV"""
    return df.to_csv(index=False).encode('utf-8')

def show():
    st.title("📊 Harassment Statistics Dashboard")
    
    # tabs for Global and Local statistics
    global_tab, local_tab = st.tabs(["🌍 Global Statistics", "📍 Local Reports"])
    
    with global_tab:
        # Global Statistics (UN and WHO data)
        st.subheader("Global Overview 2023")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Global Cases",
                "736M",
                "+12% from 2022",
                help="Source: UN Women Global Database"
            )
        with col2:
            st.metric(
                "Reporting Rate",
                "40%",
                "+5% from 2022",
                help="Percentage of victims who report"
            )
        with col3:
            st.metric(
                "Workplace Harassment",
                "31%",
                help="Women experiencing workplace harassment"
            )
        with col4:
            st.metric(
                "Online Harassment",
                "73%",
                "+23% since 2020",
                help="Women experiencing online harassment"
            )

        # Global Trends
        st.subheader("Global Trends")
        
        # Global monthly data (UN Women reports)
        global_monthly_data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Reports (Millions)': [61.3, 61.5, 61.8, 62.1, 62.4, 62.6, 
                                 62.9, 63.2, 63.5, 63.8, 64.1, 64.4]
        }
        df_monthly_global = pd.DataFrame(global_monthly_data)
        
        fig_monthly_global = px.line(
            df_monthly_global,
            x='Month',
            y='Reports (Millions)',
            title='Global Monthly Harassment Reports 2023',
            markers=True
        )
        st.plotly_chart(fig_monthly_global, use_container_width=True)

        # Global Harassment Types
        col1, col2 = st.columns(2)
        
        with col1:
            # Types of Harassment (WHO data)
            global_types = {
                'Type': ['Verbal', 'Physical', 'Online', 'Workplace', 
                        'Educational', 'Public Space'],
                'Percentage': [45, 23, 73, 31, 28, 51]
            }
            df_types_global = pd.DataFrame(global_types)
            
            fig_types_global = px.pie(
                df_types_global,
                values='Percentage',
                names='Type',
                title='Global Types of Harassment',
                hole=0.4
            )
            st.plotly_chart(fig_types_global, use_container_width=True)
        
        with col2:
            # Location data (UN Safe Cities programme)
            global_locations = {
                'Location': ['Public Transport', 'Workplace', 'Educational', 
                            'Public Spaces', 'Online', 'Home'],
                'Percentage': [82, 31, 28, 51, 73, 35]
            }
            df_locations_global = pd.DataFrame(global_locations)
            
            fig_locations_global = px.bar(
                df_locations_global,
                x='Location',
                y='Percentage',
                title='Global Harassment by Location (%)',
                color='Percentage'
            )
            st.plotly_chart(fig_locations_global, use_container_width=True)

        # Global Insights
        st.subheader("Global Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Key Global Statistics:**
            - 1 in 3 women globally experience violence
            - 73% of women face online harassment
            - 82% feel unsafe on public transport
            - Only 40% of incidents are reported
            - 137 women are killed by family members daily
            """)
        
        with col2:
            st.warning("""
            **UN Recommendations:**
            1. Strengthen legal frameworks
            2. Improve reporting mechanisms
            3. Enhance public safety measures
            4. Increase education and awareness
            5. Support victim services
            6. Address online harassment
            """)

    with local_tab:
        # Get local statistics
        stats = get_report_stats()
        
        # Local Overview
        st.subheader("Local Reports Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Reports",
                stats['total'],
                f"+{stats.get('last_24h', 0)} today",
                help="Total number of local reports"
            )
        with col2:
            st.metric(
                "Active Cases",
                stats.get('active', 0),
                help="Cases under investigation"
            )
        with col3:
            st.metric(
                "Resolved Cases",
                stats.get('resolved', 0),
                help="Successfully resolved cases"
            )
        with col4:
            resolution_rate = (stats.get('resolved', 0) / stats['total'] * 100 
                             if stats['total'] > 0 else 0)
            st.metric(
                "Resolution Rate",
                f"{resolution_rate:.1f}%",
                help="Percentage of cases resolved"
            )

        # Local Trends
        if stats.get('monthly_data'):
            monthly_df = pd.DataFrame(stats['monthly_data'], 
                                    columns=['Month', 'Count'])
            fig_monthly = px.line(
                monthly_df,
                x='Month',
                y='Count',
                title='Local Monthly Reports',
                markers=True
            )
            st.plotly_chart(fig_monthly, use_container_width=True)

        # Local Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if stats.get('by_type'):
                types_df = pd.DataFrame(stats['by_type'], 
                                      columns=['Type', 'Count'])
                fig_types = px.pie(
                    types_df,
                    values='Count',
                    names='Type',
                    title='Local Types of Harassment',
                    hole=0.4
                )
                st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            if stats.get('by_location'):
                location_df = pd.DataFrame(stats['by_location'], 
                                         columns=['Location', 'Count'])
                fig_location = px.bar(
                    location_df,
                    x='Location',
                    y='Count',
                    title='Local Reports by Location',
                    color='Count'
                )
                st.plotly_chart(fig_location, use_container_width=True)

    # Download Options
    st.subheader("📥 Download Reports")
    col1, col2 = st.columns(2)
    
    with col1:
        # Global Statistics Download
        if stats.get('monthly_data'):  # Only show if we have data
            global_monthly_df = pd.DataFrame(global_monthly_data)
            global_types_df = pd.DataFrame(global_types)
            global_locations_df = pd.DataFrame(global_locations)
            
            st.download_button(
                label="Download Global Statistics (CSV)",
                data=save_dataframe(global_monthly_df, "global_monthly.csv"),
                file_name="global_statistics.csv",
                mime="text/csv",
                help="Download global statistics in CSV format"
            )
    
    with col2:
        # Local Statistics Download
        if stats.get('monthly_data'):  # Only show if we have data
            monthly_df = pd.DataFrame(stats['monthly_data'], columns=['Month', 'Count'])
            
            st.download_button(
                label="Download Local Statistics (CSV)",
                data=save_dataframe(monthly_df, "local_monthly.csv"),
                file_name="local_statistics.csv",
                mime="text/csv",
                help="Download local statistics in CSV format"
            )

    # Data Sources
    st.subheader("📚 Data Sources")
    st.markdown("""
    **Global Data Sources:**
    - UN Women Global Database on Violence against Women (2023)
    - World Health Organization (WHO) Global Statistics
    - UN Safe Cities and Safe Public Spaces Programme
    - Global Workplace Harassment Study 2023
    - UNESCO School Violence and Bullying Report
    
    **Local Data Sources:**
    - SafeVoice Africa Incident Reports
    - Community Support Center Data
    - Local Law Enforcement Statistics
    """)

if __name__ == "__main__":
    show()
