# dashboard.py
"""
Dashboard for visualizing disease surveillance data with multiple charts.
"""
import matplotlib.pyplot as plt
import json
from data_storage import get_reports
import pandas as pd

def load_data():
    reports = get_reports()
    data = []
    for r in reports:
        d = {
            'id': r[0],
            'source': r[1],
            'patient_age': r[2],
            'patient_gender': r[3],
            'location': r[4],
            'symptoms': json.loads(r[5]) if r[5] else {},
            'report_type': r[6],
            'timestamp': r[7]
        }
        data.append(d)
    return pd.DataFrame(data)

def plot_symptom_trends(df):
    symptom_counts = {}
    for symptoms in df['symptoms']:
        for k, v in symptoms.items():
            symptom_counts[k] = symptom_counts.get(k, 0) + v
    plt.bar(symptom_counts.keys(), symptom_counts.values())
    plt.title('Total Cases by Symptom')
    plt.ylabel('Cases')
    plt.show()

def plot_cases_by_location(df):
    loc_counts = df['location'].value_counts()
    loc_counts.plot(kind='bar')
    plt.title('Cases by Location')
    plt.ylabel('Cases')
    plt.show()

def plot_demographics(df):
    df['patient_age'].dropna().astype(int).plot(kind='hist', bins=10)
    plt.title('Patient Age Distribution')
    plt.xlabel('Age')
    plt.show()
    df['patient_gender'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Gender Distribution')
    plt.ylabel('')
    plt.show()

def main():
    df = load_data()
    if df.empty:
        print('No data to display.')
        return
    plot_symptom_trends(df)
    plot_cases_by_location(df)
    plot_demographics(df)

if __name__ == "__main__":
    main()
