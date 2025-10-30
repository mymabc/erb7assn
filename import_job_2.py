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

# Input CSV file path
csv_file_path = 'job_listings_import.csv'

# Define expected columns
CSV_COLUMNS = [
    'title',
    'department',
    'summary',
    'qualifications',
    'category',
    'city',
    'is_published'
]

# Validation helpers
def is_valid_bool(value):
    return value.strip().lower() in ['true', 'false']

def is_valid_row(row):
    if len(row) != len(CSV_COLUMNS):
        return False
    title, department, summary, qualifications, category, city, is_published = [val.strip() for val in row]
    return all([
        title,
        department,
        summary,
        category,
        city,
        is_valid_bool(is_published)
    ])

def parse_row(row):
    parsed = []
    for i, col in enumerate(CSV_COLUMNS):
        val = row[i].strip()
        if col == 'is_published':
            parsed.append(val.lower() == 'true')
        else:
            parsed.append(val)
    return tuple(parsed)

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    valid_rows = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if is_valid_row(row):
                valid_rows.append(parse_row(row))
            else:
                print(f"⚠️ Skipped invalid row: {row}")

    if valid_rows:
        columns_str = ', '.join(CSV_COLUMNS)
        placeholders = ', '.join(['%s'] * len(CSV_COLUMNS))
        sql = f"INSERT INTO job_listings_job_listing ({columns_str}) VALUES ({placeholders});"
        cur.executemany(sql, valid_rows)
        conn.commit()
        print(f"✅ Imported {len(valid_rows)} valid job listings.")
    else:
        print("⚠️ No valid rows to import.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()

