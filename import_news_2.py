import csv
import psycopg2
import sys

# Database connection settings
DB_CONFIG = {
    'dbname': 'clinic_clone',
    'user': 'postgres',
    'password': '4321',
    'host': 'localhost',
    'port': '5432'
}

# Expected CSV columns
EXPECTED_COLUMNS = ['heading', 'summary', 'contents', 'is_published']

def is_valid_row(row):
    """Validate required fields and boolean format."""
    for col in EXPECTED_COLUMNS:
        if col not in row or row[col].strip() == '':
            print(f"Missing or empty value for column: {col}")
            return False
    if row['is_published'].lower() not in ['true', 'false']:
        print(f"Invalid value for is_published: {row['is_published']}")
        return False
    return True

def import_news(csv_path):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames != EXPECTED_COLUMNS:
                print("CSV header does not match expected columns.")
                return

            for row in reader:
                if not is_valid_row(row):
                    print(f"Skipping invalid row: {row}")
                    continue

                cur.execute("""
                    INSERT INTO news_article (heading, summary, contents, is_published)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row['heading'],
                    row['summary'],
                    row['contents'],
                    row['is_published'].lower() == 'true'
                ))

        conn.commit()
        print("Import completed successfully.")

    except Exception as e:
        print(f"Error during import: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python import_news_2.py path/to/news.csv")
    else:
        import_news(sys.argv[1])

