import streamlit as st
import pandas as pd
from datetime import datetime

# Sample resource data 
RESOURCES = {
    "Emergency Contacts": [
        {
            "name": "National Emergency Number",
            "contact": "112",
            "description": "24/7 Emergency Services",
            "category": "Emergency"
        },
        {
            "name": "Women's Helpline",
            "contact": "1091",
            "description": "24/7 Women's Emergency Helpline",
            "category": "Emergency"
        }
    ],
    "Legal Resources": [
        {
            "name": "Legal Aid Services",
            "contact": "1516",
            "description": "Free legal consultation and support",
            "category": "Legal"
        },
        {
            "name": "Cyber Crime Portal",
            "contact": "cybercrime.gov.in",
            "description": "Online portal for reporting cyber crimes",
            "category": "Legal"
        }
    ],
    "Support Organizations": [
        {
            "name": "Counseling Services",
            "contact": "1800-XXX-XXXX",
            "description": "Professional counseling support",
            "category": "Support"
        },
        {
            "name": "NGO Helpline",
            "contact": "1800-XXX-XXXX",
            "description": "NGO support services",
            "category": "Support"
        }
    ]
}

#  new resource dictionaries
AFRICAN_EMERGENCY_CONTACTS = {
    "south_africa": {
        "country_code": "+27",
        "emergency": {
            "police": "10111",
            "ambulance": "10177",
            "fire": "10177",
            "general": "112"
        },
        "hospitals": [
            {
                "name": "Netcare Hospitals",
                "phone": "+27 11 301 0000",
                "locations": "Multiple locations"
            },
            {
                "name": "Mediclinic",
                "phone": "+27 21 809 6500",
                "locations": "Multiple locations"
            }
        ]
    },
    "kenya": {
        "country_code": "+254",
        "emergency": {
            "police": "999",
            "ambulance": "999",
            "fire": "999",
            "general": "112",
            "gender_violence": "1195",
            "child_helpline": "116"
        },
        "hospitals": [
            {
                "name": "Nairobi Hospital",
                "phone": "+254 20 2845000",
                "location": "Nairobi"
            },
            {
                "name": "Aga Khan University Hospital",
                "phone": "+254 20 3662000",
                "location": "Nairobi"
            }
        ]
    },
    "uganda": {
        "country_code": "+256",
        "emergency": {
            "police": "999",
            "ambulance": "911",
            "fire": "112",
            "general": "112",
            "child_helpline": "116"
        },
        "hospitals": [
            {
                "name": "Mulago National Referral Hospital",
                "phone": "+256 414 541 577",
                "location": "Kampala"
            },
            {
                "name": "International Hospital Kampala",
                "phone": "+256 312 200 400",
                "location": "Kampala"
            }
        ]
    },
    "tanzania": {
        "country_code": "+255",
        "emergency": {
            "police": "112",
            "ambulance": "112",
            "fire": "114",
            "general": "112",
            "gender_violence": "116"
        },
        "hospitals": [
            {
                "name": "Muhimbili National Hospital",
                "phone": "+255 22 2151367",
                "location": "Dar es Salaam"
            },
            {
                "name": "Aga Khan Hospital",
                "phone": "+255 22 2115151",
                "location": "Dar es Salaam"
            }
        ]
    },
    "rwanda": {
        "country_code": "+250",
        "emergency": {
            "police": "112",
            "ambulance": "912",
            "fire": "112",
            "general": "112",
            "gender_violence": "3512"
        },
        "hospitals": [
            {
                "name": "King Faisal Hospital",
                "phone": "+250 788 123 200",
                "location": "Kigali"
            },
            {
                "name": "Rwanda Military Hospital",
                "phone": "+250 788 305 703",
                "location": "Kigali"
            }
        ]
    },
    "ethiopia": {
        "country_code": "+251",
        "emergency": {
            "police": "911",
            "ambulance": "907",
            "fire": "939",
            "general": "911"
        },
        "hospitals": [
            {
                "name": "Black Lion Hospital",
                "phone": "+251 115 538 880",
                "location": "Addis Ababa"
            },
            {
                "name": "St. Paul's Hospital",
                "phone": "+251 111 111 111",
                "location": "Addis Ababa"
            }
        ]
    },
    "nigeria": {
        "country_code": "+234",
        "emergency": {
            "police": "112",
            "ambulance": "112",
            "fire": "112",
            "general": "112",
            "nema": "0800-2255-6362"
        },
        "hospitals": [
            {
                "name": "National Hospital Abuja",
                "phone": "+234 9 524 6690",
                "location": "Abuja"
            },
            {
                "name": "Lagos University Teaching Hospital",
                "phone": "+234 1 773 0190",
                "location": "Lagos"
            }
        ]
    }
}

WOMEN_EMERGENCY_CONTACTS = {
    "south_africa": {
        "hotlines": {
            "gender_violence": "0800 150 150",
            "rape_crisis": "021 447 9762",
            "people_against_abuse": "0800 150 150",
            "childline": "0800 055 555"
        },
        "organizations": [
            {
                "name": "Women's Legal Centre",
                "phone": "+27 21 424 5660",
                "website": "https://wlce.co.za",
                "services": ["legal_aid", "counseling", "advocacy"]
            }
        ]
    },
}

GLOBAL_EMERGENCY_NUMBERS = {
    "united_states": {
        "country_code": "+1",
        "emergency": {
            "general": "911",
            "domestic_violence": "1-800-799-7233",
            "suicide_prevention": "988",
            "human_trafficking": "1-888-373-7888"
        }
    },
    "united_kingdom": {
        "country_code": "+44",
        "emergency": {
            "general": "999",
            "non_emergency": "101",
            "domestic_violence": "0808 2000 247",
            "rape_crisis": "0808 802 9999"
        }
    },
    "india": {
        "country_code": "+91",
        "emergency": {
            "general": "112",
            "women_helpline": "1091",
            "domestic_violence": "181",
            "police": "100"
        }
    },
    "australia": {
        "country_code": "+61",
        "emergency": {
            "general": "000",
            "domestic_violence": "1800 737 732",
            "mental_health": "13 11 14"
        }
    }
}

WOMEN_SAFETY_RESOURCES = {
    "global_hotlines": {
        "un_women": {
            "name": "UN Women",
            "contact": "+1 646-781-4400",
            "website": "https://www.unwomen.org",
            "services": ["advocacy", "support", "resources"]
        },
        "international_womens_rights": {
            "name": "Equality Now",
            "contact": "+1 212-586-0906",
            "website": "https://www.equalitynow.org",
            "services": ["legal_aid", "advocacy", "support"]
        }
    },
    "harassment_reporting": {
        "workplace": [
            {
                "name": "Equal Employment Opportunity Commission (US)",
                "contact": "1-800-669-4000",
                "website": "https://www.eeoc.gov",
                "type": "workplace_harassment"
            },
            {
                "name": "Working Women's Helpline (India)",
                "contact": "1091",
                "type": "workplace_harassment"
            }
        ],
        "online": [
            {
                "name": "Cyber Civil Rights Initiative",
                "contact": "1-844-878-2274",
                "website": "https://www.cybercivilrights.org",
                "type": "cyber_harassment"
            },
            {
                "name": "National Cyber Crime Reporting Portal (India)",
                "website": "https://cybercrime.gov.in",
                "type": "cyber_harassment"
            }
        ],
        "public_spaces": [
            {
                "name": "Hollaback!",
                "website": "https://www.ihollaback.org",
                "type": "street_harassment",
                "resources": ["reporting", "training", "support"]
            }
        ]
    },
 
    "legal_resources": {
        "international": [
            {
                "name": "International Association of Women Judges",
                "website": "https://www.iawj.org",
                "services": ["legal_support", "advocacy"]
            },
            {
                "name": "Women's Link Worldwide",
                "website": "https://www.womenslinkworldwide.org",
                "services": ["legal_aid", "advocacy"]
            }
        ]
    },
    "support_networks": {
        "education": [
            {
                "name": "Girls Who Code",
                "website": "https://girlswhocode.com",
                "type": "tech_education"
            },
            {
                "name": "Malala Fund",
                "website": "https://malala.org",
                "type": "education_rights"
            }
        ],
        "professional": [
            {
                "name": "Professional Women's Network",
                "website": "https://pwnglobal.net",
                "type": "professional_development"
            }
        ]
    }
}

HARASSMENT_RESPONSE_GUIDELINES = {
    "immediate_steps": [
        "Find a safe location",
        "Contact emergency services if in immediate danger",
        "Document the incident (time, location, details)",
        "Seek medical attention if needed",
        "Contact a trusted person"
    ],
    "reporting_process": [
        "File a police report",
        "Report to relevant authorities (work/school/etc.)",
        "Gather evidence (photos, messages, witnesses)",
        "Keep copies of all documentation",
        "Seek legal counsel if needed"
    ],
    "support_resources": [
        "Counseling services",
        "Legal aid organizations",
        "Support groups",
        "Advocacy organizations",
        "Online support communities"
    ]
}

# Updated  RESOURCES dictionary
RESOURCES.update({
    "African Emergency Contacts": [
        {
            "name": f"{country.title()} Emergency Services",
            "contact": details["emergency"]["general"],
            "description": f"General emergency number for {country.title()}",
            "category": "Emergency"
        }
        for country, details in AFRICAN_EMERGENCY_CONTACTS.items()
        if "emergency" in details and "general" in details["emergency"]
    ],
    "Women's Emergency Services": [
        {
            "name": f"{country.title()} - {org['name']}",
            "contact": org["phone"],
            "description": f"Services: {', '.join(org['services'])}",
            "category": "Women Support",
            "website": org.get("website", "")
        }
        for country, details in WOMEN_EMERGENCY_CONTACTS.items()
        for org in details.get("organizations", [])
    ],
    "Women's Hotlines": [
        {
            "name": f"{country.title()} - {hotline_type.replace('_', ' ').title()}",
            "contact": number,
            "description": f"Emergency hotline for {hotline_type.replace('_', ' ')} in {country.title()}",
            "category": "Women Support"
        }
        for country, details in WOMEN_EMERGENCY_CONTACTS.items()
        for hotline_type, number in details.get("hotlines", {}).items()
    ],
    "Global Emergency": [
        {
            "name": f"{country.replace('_', ' ').title()} Emergency Services",
            "contact": details["emergency"]["general"],
            "description": f"General emergency number for {country.replace('_', ' ').title()}",
            "category": "Emergency"
        }
        for country, details in GLOBAL_EMERGENCY_NUMBERS.items()
    ],
    "Women Safety": [
        {
            "name": org["name"],
            "contact": org.get("contact", "See website"),
            "description": f"Services: {', '.join(org['services'])}",
            "category": "Women Safety",
            "website": org["website"]
        }
        for category in WOMEN_SAFETY_RESOURCES.values()
        for org in (category if isinstance(category, list) else [category])
        if isinstance(org, dict) and "name" in org
    ]
})

def show_resource_category(category, resources):
    """Display resources for a specific category"""
    st.subheader(f"📚 {category}")
    
    for resource in resources:
        with st.expander(f"🔍 {resource['name']}"):
            st.write(f"**Contact:** {resource['contact']}")
            st.write(f"**Description:** {resource['description']}")
            
            # copy button for contact
            if st.button(f"Copy Contact", key=f"copy_{resource['name']}"):
                st.write(f"📋 Copied: {resource['contact']}")
                st.toast(f"Contact copied: {resource['contact']}")

def show_emergency_resources():
    """Display emergency resources section"""
    st.error("🚨 **EMERGENCY RESOURCES**")
    
    # country selector for African emergency numbers
    selected_country = st.selectbox(
        "Select Country",
        options=list(AFRICAN_EMERGENCY_CONTACTS.keys()),
        format_func=lambda x: x.title()
    )
    
    # Display emergency numbers for selected country
    if selected_country in AFRICAN_EMERGENCY_CONTACTS:
        country_data = AFRICAN_EMERGENCY_CONTACTS[selected_country]
        cols = st.columns(len(country_data["emergency"]))
        for col, (service, number) in zip(cols, country_data["emergency"].items()):
            with col:
                st.button(
                    f"📞 {service.upper()} ({number})", 
                    use_container_width=True
                )

    #  women's emergency numbers
    if selected_country in WOMEN_EMERGENCY_CONTACTS:
        st.error("🚺 **WOMEN'S EMERGENCY CONTACTS**")
        women_data = WOMEN_EMERGENCY_CONTACTS[selected_country]
        if "hotlines" in women_data:
            cols = st.columns(len(women_data["hotlines"]))
            for col, (service, number) in zip(cols, women_data["hotlines"].items()):
                with col:
                    st.button(
                        f"🆘 {service.replace('_', ' ').upper()} ({number})",
                        use_container_width=True
                    )

def show_harassment_guidelines():
    """Display harassment response guidelines"""
    st.subheader("🛡️ Harassment Response Guidelines")
    
    tabs = st.tabs(["Immediate Steps", "Reporting Process", "Support Resources"])
    
    with tabs[0]:
        for step in HARASSMENT_RESPONSE_GUIDELINES["immediate_steps"]:
            st.write(f"• {step}")
    
    with tabs[1]:
        for step in HARASSMENT_RESPONSE_GUIDELINES["reporting_process"]:
            st.write(f"• {step}")
    
    with tabs[2]:
        for resource in HARASSMENT_RESPONSE_GUIDELINES["support_resources"]:
            st.write(f"• {resource}")

def show():
    st.title("📚 Resources & Support")
    
    st.markdown("""
    Access important contacts, support services, and resources. 
    In case of emergency, please contact emergency services immediately.
    """)
    
    # Show emergency resources at the top
    show_emergency_resources()
    
    # search functionality
    st.subheader("🔍 Search Resources")
    search_term = st.text_input("Search for specific resources:")
    
    # Filter resources based on search
    filtered_resources = RESOURCES.copy()
    if search_term:
        filtered_resources = {
            category: [
                resource for resource in resources
                if search_term.lower() in resource['name'].lower() or 
                   search_term.lower() in resource['description'].lower()
            ]
            for category, resources in RESOURCES.items()
        }
        # Remove empty categories
        filtered_resources = {k: v for k, v in filtered_resources.items() if v}
    
    # Display resources by category
    for category, resources in filtered_resources.items():
        if resources:  # Only show categories with resources
            st.divider()
            show_resource_category(category, resources)
    
    #  harassment guidelines section
    st.divider()
    show_harassment_guidelines()
    
    # resource submission form
    st.sidebar.subheader("📝 Submit New Resource")
    with st.sidebar.form("resource_submission"):
        new_resource_name = st.text_input("Resource Name")
        new_resource_contact = st.text_input("Contact Information")
        new_resource_category = st.selectbox(
            "Category",
            ["Emergency Contacts", "Legal Resources", "Support Organizations", 
             "Global Emergency", "Women Safety", "Harassment Response",
             "Support Networks"]
        )
        new_resource_description = st.text_area("Description")
        
        if st.form_submit_button("Submit Resource"):
            st.success("Thank you for submitting a resource! It will be reviewed.")
    
    # download option for resources
    st.sidebar.subheader("📥 Download Resources")
    if st.sidebar.button("Download Resource List"):
        # Convert resources to DataFrame
        resource_list = []
        for category, resources in RESOURCES.items():
            for resource in resources:
                resource_list.append({
                    "Category": category,
                    "Name": resource['name'],
                    "Contact": resource['contact'],
                    "Description": resource['description']
                })
        
        df = pd.DataFrame(resource_list)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.sidebar.download_button(
            "Download CSV",
            csv,
            "support_resources.csv",
            "text/csv",
            key='download-csv'
        )
    
    # feedback section
    st.sidebar.divider()
    st.sidebar.subheader("📢 Feedback")
    if st.sidebar.button("Share Feedback"):
        st.sidebar.text_area("Your feedback helps us improve")
        st.sidebar.button("Submit Feedback")

if __name__ == "__main__":
    show()
