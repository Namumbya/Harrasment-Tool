import sqlite3
from sqlite3 import Error

def insert_sample_data():
    try:
        connection = sqlite3.connect('harassment_tool.db')
        cursor = connection.cursor()
        
        # Sample data for resources in Africa
        resources_data = [
            # Kenya
            (
                'Gender Violence Recovery Centre',
                'Medical',
                '+254 719 638 006',
                'Nairobi Women\'s Hospital, Hurlingham, Nairobi',
                -1.2921,
                36.8219,
                'Provides comprehensive care for survivors of gender-based violence'
            ),
            (
                'FIDA Kenya',
                'Legal',
                '+254 722 509 760',
                'Amboseli Road, Off Gitanga Road, Lavington, Nairobi',
                -1.2924,
                36.7660,
                'Federation of Women Lawyers providing legal aid and advocacy'
            ),
            
            # South Africa
            (
                'Rape Crisis Cape Town Trust',
                'Support',
                '+27 21 447 1467',
                'Observatory, Cape Town',
                -33.9249,
                18.4241,
                '24-hour crisis support and counseling services'
            ),
            (
                'People Opposing Women Abuse (POWA)',
                'Support',
                '+27 11 642 4345',
                'Johannesburg, Gauteng',
                -26.2041,
                28.0473,
                'Support services for women experiencing domestic violence'
            ),
            
            # Nigeria
            (
                'Women\'s Rights Advancement and Protection Alternative',
                'Legal',
                '+234 9 876 5432',
                'Abuja, Federal Capital Territory',
                9.0765,
                7.3986,
                'Legal support and advocacy for women\'s rights'
            ),
            (
                'WARIF Centre',
                'Medical',
                '+234 809 210 0009',
                'Lagos State',
                6.5244,
                3.3792,
                'Women At Risk International Foundation - 24/7 confidential support'
            ),
            
            # Uganda
            (
                'Action Aid Uganda',
                'Support',
                '+256 392 220 002',
                'Kampala',
                0.3476,
                32.5825,
                'Support services and empowerment programs for women'
            ),
            
            # Ghana
            (
                'Domestic Violence and Victim Support Unit',
                'Police',
                '+233 302 773 906',
                'Accra Central',
                5.5560,
                -0.1969,
                'Specialized police unit handling domestic violence cases'
            ),
            
            # Tanzania
            (
                'Tanzania Women Lawyers Association',
                'Legal',
                '+255 22 2862865',
                'Dar es Salaam',
                -6.7924,
                39.2083,
                'Legal aid and support for women and children'
            ),
            
            # Rwanda
            (
                'Isange One Stop Centre',
                'Medical',
                '+250 788 311 555',
                'Kigali',
                -1.9441,
                30.0619,
                'Comprehensive support for GBV victims including medical, police, and counseling'
            ),
            
            # Ethiopia
            (
                'Ethiopian Women Lawyers Association',
                'Legal',
                '+251 11 550 6641',
                'Addis Ababa',
                9.0320,
                38.7421,
                'Legal aid and advocacy for women\'s rights'
            ),
            
            # Pan-African Hotlines
            (
                'African Women\'s Development Fund',
                'Support',
                '+233 302 521 257',
                'Accra, Ghana (Serving all Africa)',
                5.6037,
                -0.1870,
                'Grant-making foundation supporting women\'s rights organizations'
            )
        ]
        
        # Insert data
        cursor.executemany('''
            INSERT INTO resources (name, type, contact, address, latitude, longitude, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', resources_data)
        
        connection.commit()
        print(f"Successfully inserted {len(resources_data)} resources!")
        
    except Error as error:
        print("Error while inserting data:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SQLite connection closed")

if __name__ == "__main__":
    insert_sample_data() 