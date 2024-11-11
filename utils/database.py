import sqlite3
import os

def init_db():
    """Initialize the database with all necessary tables"""
    os.makedirs('data', exist_ok=True)
    
    conn = get_db()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  name TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Reports table
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  type TEXT,
                  description TEXT,
                  location TEXT,
                  timestamp TEXT,
                  status TEXT DEFAULT 'pending',
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    os.makedirs('data', exist_ok=True)
    return sqlite3.connect('data/database.db')

def execute_query(query, params=(), fetchone=False):
    """Execute database query with error handling"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if query.strip().upper().startswith('SELECT'):
            if fetchone:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return result
            
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_reports(user_id=None):
    """Get all reports or reports for a specific user"""
    query = "SELECT * FROM reports"
    params = ()
    
    if user_id:
        query += " WHERE user_id = ?"
        params = (user_id,)
    
    query += " ORDER BY timestamp DESC"
    return execute_query(query, params)

def add_report(user_id, type, description, location):
    """Add a new report"""
    query = """
        INSERT INTO reports (user_id, type, description, location, timestamp, status)
        VALUES (?, ?, ?, ?, datetime('now'), 'pending')
    """
    return execute_query(query, (user_id, type, description, location))

def get_report_stats():
    """Get comprehensive report statistics"""
    stats = {}
    
    try:
        # Basic stats
        stats['total'] = execute_query(
            "SELECT COUNT(*) FROM reports", 
            fetchone=True
        )[0]
        
        # Last 24 hours
        stats['last_24h'] = execute_query("""
            SELECT COUNT(*) FROM reports 
            WHERE timestamp > datetime('now', '-1 day')
        """, fetchone=True)[0]
        
        # Status counts
        stats['active'] = execute_query("""
            SELECT COUNT(*) FROM reports 
            WHERE status = 'active'
        """, fetchone=True)[0]
        
        stats['resolved'] = execute_query("""
            SELECT COUNT(*) FROM reports 
            WHERE status = 'resolved'
        """, fetchone=True)[0]
        
        # Type distribution
        stats['by_type'] = execute_query("""
            SELECT type, COUNT(*) as count 
            FROM reports 
            GROUP BY type 
            ORDER BY count DESC
        """)
        
        # Location distribution
        stats['by_location'] = execute_query("""
            SELECT location, COUNT(*) as count 
            FROM reports 
            GROUP BY location 
            ORDER BY count DESC
        """)
        
        # Time analysis
        stats['by_time'] = execute_query("""
            SELECT strftime('%H', timestamp) as hour, 
                   COUNT(*) as count 
            FROM reports 
            GROUP BY hour 
            ORDER BY hour
        """)
        
        # Monthly trends
        stats['monthly_data'] = execute_query("""
            SELECT strftime('%Y-%m', timestamp) as month, 
                   COUNT(*) as count 
            FROM reports 
            GROUP BY month 
            ORDER BY month
        """)
        
        # Get top type
        if stats.get('by_type') and len(stats['by_type']) > 0:
            stats['top_type'] = stats['by_type'][0][0]
        
        # Get peak time
        if stats.get('by_time') and len(stats['by_time']) > 0:
            peak_hour = max(stats['by_time'], key=lambda x: x[1])[0]
            stats['peak_time'] = f"{int(peak_hour):02d}:00"
        
        # Get top location
        if stats.get('by_location') and len(stats['by_location']) > 0:
            stats['top_location'] = stats['by_location'][0][0]
        
    except Exception as e:
        print(f"Error getting statistics: {str(e)}")
        return {
            'total': 0,
            'last_24h': 0,
            'active': 0,
            'resolved': 0,
            'by_type': [],
            'by_location': [],
            'by_time': [],
            'monthly_data': []
        }
        
    return stats
