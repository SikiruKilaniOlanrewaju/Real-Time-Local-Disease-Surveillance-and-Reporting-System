from flask import Flask, render_template, request, redirect, url_for
import data_storage
import data_collection
import json
import dashboard
import os

app = Flask(__name__)

def ensure_db():
    if not os.path.exists('health_data.db'):
        data_storage.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Collect form data
        patient_age = request.form.get('patient_age')
        patient_gender = request.form.get('patient_gender')
        location = request.form.get('location')
        report_type = request.form.get('report_type')
        fever = request.form.get('fever')
        cough = request.form.get('cough')
        headache = request.form.get('headache')
        symptoms = {}
        if fever and fever.isdigit():
            symptoms['fever'] = int(fever)
        if cough and cough.isdigit():
            symptoms['cough'] = int(cough)
        if headache and headache.isdigit():
            symptoms['headache'] = int(headache)
        data_storage.store_report(
            source=report_type or 'unknown',
            symptoms=json.dumps(symptoms),
            patient_age=int(patient_age) if patient_age and patient_age.isdigit() else None,
            patient_gender=patient_gender,
            location=location,
            report_type=report_type
        )
        return redirect(url_for('index'))
    return render_template('submit.html')

@app.route('/dashboard')
def show_dashboard():
    # This will just call the dashboard script for now
    # In a real app, you would render charts directly
    dashboard.main()
    return "Dashboard generated. Please check the pop-up windows for charts."

if __name__ == '__main__':
    ensure_db()
    app.run(debug=True)
