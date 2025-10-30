import psycopg2
import csv

# Database configuration
DB_CONFIG = {
    'dbname': 'clinic_clone',
    'user': 'postgres',
    'password': '4321',
    'host': 'localhost',
    'port': '5432'
}

# Output CSV file path
csv_file_path = 'job_listings_export.csv'

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Get all column names from the table
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'job_listings_job_listing'
        ORDER BY ordinal_position;
    """)
    columns = [row[0] for row in cur.fetchall()]
    column_list = ', '.join(columns)

    # Fetch all data
    cur.execute(f"SELECT {column_list} FROM job_listings_job_listing;")
    rows = cur.fetchall()

    # Write to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Header
        writer.writerows(rows)    # Data

    print(f"✅ Exported {len(rows)} records to '{csv_file_path}'.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()

