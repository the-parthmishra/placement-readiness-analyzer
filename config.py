import mysql.connector

# -----------------------------------------------
# Company-wise skill weights (must add up to 1.0)
# -----------------------------------------------
WEIGHTS = {
    "product": {
        "DSA": 0.4, "OS": 0.2, "DBMS": 0.15,
        "CN": 0.15, "Aptitude": 0.05, "Communication": 0.05
    },
    "service": {
        "DSA": 0.1, "OS": 0.1, "DBMS": 0.2,
        "CN": 0.1, "Aptitude": 0.4, "Communication": 0.1
    },
    "core": {
        "DSA": 0.2, "OS": 0.2, "DBMS": 0.2,
        "CN": 0.3, "Aptitude": 0.05, "Communication": 0.05
    }
}

# Minimum score to be considered "ready" in a category
THRESHOLD = 0.6

# -----------------------------------------------
# Database connection function
# -----------------------------------------------
def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your-mySQL-pass",        
            database="placement_tool"
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None
