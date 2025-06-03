import data_collection
import data_storage
import data_analysis
import visualization
import reporting
import json

print("Hello, World!")

if __name__ == "__main__":
    # Initialize database
    data_storage.init_db()
    # Collect data interactively
    clinic = data_collection.collect_from_clinic()
    mobile = data_collection.collect_from_mobile()
    # Store collected data with new attributes
    data_storage.store_report(
        source="clinic",
        symptoms=json.dumps(clinic["symptoms"]),
        patient_age=clinic["patient_age"],
        patient_gender=clinic["patient_gender"],
        location=clinic["location"],
        report_type=clinic["report_type"]
    )
    data_storage.store_report(
        source="mobile",
        symptoms=json.dumps(mobile["symptoms"]),
        patient_age=mobile["patient_age"],
        patient_gender=mobile["patient_gender"],
        location=mobile["location"],
        report_type=mobile["report_type"]
    )
    # Analyze data
    reports = data_storage.get_reports()
    analysis = data_analysis.analyze_reports(reports)
    # Visualize data
    visualization.plot_total_cases(analysis["total_cases"])
    # Generate report and send alert if needed
    reporting.generate_report(analysis)
    if analysis["total_cases"] > 10:
        reporting.send_alert("Potential outbreak detected!")
