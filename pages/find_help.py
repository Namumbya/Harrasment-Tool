import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import pandas as pd

# Sample emergency resources database
EMERGENCY_RESOURCES = {
    "Police Stations": [
        {"name": "Central Police Station", "address": "123 Main St", "phone": "100", "lat": 28.6139, "lon": 77.2090},
        {"name": "City Police HQ", "address": "456 Park Ave", "phone": "100", "lat": 28.6129, "lon": 77.2295},
    ],
    "Hospitals": [
        {"name": "General Hospital", "address": "789 Health Rd", "phone": "102", "lat": 28.6356, "lon": 77.2217},
        {"name": "Emergency Care Center", "address": "321 Care Lane", "phone": "102", "lat": 28.6100, "lon": 77.2300},
    ],
    "Support Centers": [
        {"name": "Women's Help Center", "address": "555 Support St", "phone": "1091", "lat": 28.6200, "lon": 77.2100},
        {"name": "Crisis Center", "address": "777 Hope Rd", "phone": "1098", "lat": 28.6150, "lon": 77.2200},
    ]
}

def get_location():
    """Get user's location"""
    st.subheader("📍 Your Location")
    
    location_method = st.radio(
        "How would you like to set your location?",
        ["Enter Address", "Use Current Location"]
    )
    
    if location_method == "Enter Address":
        address = st.text_input("Enter your address:")
        if address:
            try:
                geolocator = Nominatim(user_agent="harassment_support_tool")
                location = geolocator.geocode(address)
                if location:
                    return location.latitude, location.longitude
                else:
                    st.error("Location not found. Please try a different address.")
            except Exception as e:
                st.error(f"Error finding location: {str(e)}")
    else:
        st.info("Please allow location access when prompted")
        try:
            location = st.experimental_get_geolocation()
            return location['latitude'], location['longitude']
        except Exception:
            st.error("Unable to access location. Please enter address manually.")
    
    return None

def create_map(lat, lon, resources):
    """Create map with nearby resources"""
    m = folium.Map(location=[lat, lon], zoom_start=13)
    
    # user location marker
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # resource markers
    for category, locations in resources.items():
        for location in locations:
            folium.Marker(
                [location['lat'], location['lon']],
                popup=f"""
                <b>{location['name']}</b><br>
                📞 {location['phone']}<br>
                📍 {location['address']}
                """,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
    
    return m

def show_resource_list(resources):
    """Display list of resources"""
    st.subheader("📋 Available Resources")
    
    for category, locations in resources.items():
        with st.expander(f"🏢 {category}"):
            for location in locations:
                st.markdown(f"""
                **{location['name']}**
                - 📞 Phone: {location['phone']}
                - 📍 Address: {location['address']}
                """)

def show():
    st.title("🔍 Find Help Near You")
    
    st.markdown("""
    Locate emergency services and support resources in your area. 
    Enter your location or use your current location to find nearby help.
    """)
    
    # Emergency notice
    st.error("""
    🚨 **In immediate danger?**
    Call Emergency Services: 911 (or your local emergency number)
    """)
    
    # Get user location
    location = get_location()
    
    if location:
        lat, lon = location
        
        # Resource type selection
        selected_resources = st.multiselect(
            "Select types of resources to display:",
            options=list(EMERGENCY_RESOURCES.keys()),
            default=list(EMERGENCY_RESOURCES.keys())
        )
        
        # Filtering resources based on selection
        filtered_resources = {k: v for k, v in EMERGENCY_RESOURCES.items() if k in selected_resources}
        
        # Creating tabs for map and list views
        tab1, tab2 = st.tabs(["🗺️ Map View", "📋 List View"])
        
        with tab1:
            st.subheader("🗺️ Nearby Resources")
            m = create_map(lat, lon, filtered_resources)
            st_folium(m, width=800, height=500)
        
        with tab2:
            show_resource_list(filtered_resources)
        
        # downloading option
        if st.button("📥 Download Resource List"):
            # Converting resources to DataFrame
            data = []
            for category, locations in filtered_resources.items():
                for location in locations:
                    data.append({
                        "Category": category,
                        "Name": location['name'],
                        "Phone": location['phone'],
                        "Address": location['address']
                    })
            
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "Download CSV",
                csv,
                "nearby_resources.csv",
                "text/csv",
                key='download-csv'
            )
    
    # Sidebar with quick access numbers
    with st.sidebar:
        st.subheader("☎️ Emergency Contacts")
        st.markdown("""
        - Police: 100
        - Ambulance: 102
        - Women's Helpline: 1091
        - Child Helpline: 1098
        - National Emergency: 112
        """)

if __name__ == "__main__":
    show()
