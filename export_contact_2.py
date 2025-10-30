import csv
import psycopg2
import sys

# Database connection configuration
DB_CONFIG = {
    'dbname': 'clinic_clone',
    'user': 'postgres',
    'password': '4321',
    'host': 'localhost',
    'port': '5432'
}

# Columns to export (excluding 'id' if not needed)
COLUMNS = ['id', 'listing', 'listing_id', 'name', 'email', 'phone', 'message', 'user_id']

def export_contacts(csv_file_path):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Build SQL query
        query = f"SELECT {', '.join(COLUMNS)} FROM contacts_contact"
        cur.execute(query)
        rows = cur.fetchall()

        # Write to CSV
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COLUMNS)  # Write header
            writer.writerows(rows)    # Write data

        print(f"Export completed successfully to {csv_file_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python export_contact_2.py path/to/output.csv")
    else:
        export_contacts(sys.argv[1])

