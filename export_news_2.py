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

# Columns to export (must match import script)
COLUMNS = ['heading', 'summary', 'contents', 'is_published']

def export_news(csv_file_path):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Build SQL query
        query = f"SELECT {', '.join(COLUMNS)} FROM news_article"
        cur.execute(query)
        rows = cur.fetchall()

        # Write to CSV with quoting and UTF-8 encoding
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(COLUMNS)  # Write header
            for row in rows:
                formatted_row = [
                    str(row[0]),  # heading
                    str(row[1]),  # summary
                    str(row[2]),  # contents
                    'True' if row[3] else 'False'  # is_published
                ]
                writer.writerow(formatted_row)

        print(f"Export completed successfully to {csv_file_path}")

    except Exception as e:
        print(f"Error during export: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python export_news.py path/to/output.csv")
    else:
        export_news(sys.argv[1])

