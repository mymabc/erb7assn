import csv
import psycopg2
import re
import sys

# Database connection configuration
DB_CONFIG = {
    'dbname': 'clinic_clone',
    'user': 'postgres',
    'password': '4321',
    'host': 'localhost',
    'port': '5432'
}

# Expected CSV columns
COLUMNS = ['listing', 'listing_id', 'name', 'email', 'phone', 'message', 'user_id']

# Email validation regex
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_row(row):
    """Validate required fields and email format."""
    for field in COLUMNS:
        if not row.get(field):
            print(f"Missing value for required field: {field}")
            return False
    if not EMAIL_REGEX.match(row['email']):
        print(f"Invalid email format: {row['email']}")
        return False
    return True

def import_contacts(csv_file_path):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames != COLUMNS:
                print("CSV header does not match expected columns.")
                return

            for row in reader:
                if not is_valid_row(row):
                    print(f"Skipping invalid row: {row}")
                    continue

                cur.execute("""
                    INSERT INTO contacts_contact (listing, listing_id, name, email, phone, message, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['listing'],
                    int(row['listing_id']),
                    row['name'],
                    row['email'],
                    row['phone'],
                    row['message'],
                    int(row['user_id'])
                ))

        conn.commit()
        print("Import completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python import_contact_2.py path/to/contacts.csv")
    else:
        import_contacts(sys.argv[1])

