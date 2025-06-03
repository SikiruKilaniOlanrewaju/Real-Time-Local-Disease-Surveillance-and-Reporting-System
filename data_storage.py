# data_storage.py
"""
Module for storing and retrieving health data. Uses SQLite for simplicity.
"""
import csv
import sqlite3

def init_db(db_name="health_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        case_id TEXT PRIMARY KEY,
        report_date TEXT,
        location TEXT,
        disease_name TEXT,
        symptoms TEXT,
        diagnosis_status TEXT,
        patient_age INTEGER,
        patient_sex TEXT,
        health_facility TEXT,
        report_source TEXT
    )''')
    conn.commit()
    conn.close()

def store_report(case_id, report_date, location, disease_name, symptoms, diagnosis_status, patient_age, patient_sex, health_facility, report_source, db_name="health_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO reports (case_id, report_date, location, disease_name, symptoms, diagnosis_status, patient_age, patient_sex, health_facility, report_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (case_id, report_date, location, disease_name, symptoms, diagnosis_status, patient_age, patient_sex, health_facility, report_source))
    conn.commit()
    conn.close()

def get_reports(db_name="health_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    results = c.fetchall()
    conn.close()
    return results

def import_from_csv(csv_path, db_name="health_data.db"):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            store_report(
                row['case_id'],
                row['report_date'],
                row['location'],
                row['disease_name'],
                row['symptoms'],
                row['diagnosis_status'],
                int(row['patient_age']) if row['patient_age'] else None,
                row['patient_sex'],
                row['health_facility'],
                row.get('entry_method', row.get('report_source', ''))
            )

if __name__ == "__main__":
    from data_storage import import_from_csv, init_db
    init_db()
    import_from_csv('sample_disease_surveillance_data.csv')
    print('Sample data imported.')
    # Example usage
    store_report("1", "2023-10-05", "NY", "flu", "{'fever': 5, 'cough': 3}", "diagnosed", 30, "M", "NY Health Clinic", "clinic")
    print(get_reports())
