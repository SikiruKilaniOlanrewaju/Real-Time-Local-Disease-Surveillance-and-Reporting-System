# data_collection.py
"""
Module for collecting health data from various sources (APIs, files, manual input, sensors).
"""

def collect_patient_info():
    """
    Collects patient metadata (age, gender, location, report type) via user input.
    Returns a dict with the info.
    """
    age = input("Patient age: ")
    gender = input("Patient gender (M/F/Other): ")
    location = input("Location: ")
    report_type = input("Report type (clinic/mobile): ")
    return {
        "patient_age": int(age) if age.isdigit() else None,
        "patient_gender": gender.strip() or None,
        "location": location.strip() or None,
        "report_type": report_type.strip() or None
    }

def collect_from_clinic():
    """
    Collect data from a clinic via user input.
    Returns a dictionary of symptom counts and patient info.
    """
    symptoms = {}
    print("Enter clinic data (leave blank to skip a symptom):")
    fever = input("Number of fever cases: ")
    cough = input("Number of cough cases: ")
    headache = input("Number of headache cases: ")
    if fever.isdigit():
        symptoms["fever"] = int(fever)
    if cough.isdigit():
        symptoms["cough"] = int(cough)
    if headache.isdigit():
        symptoms["headache"] = int(headache)
    info = collect_patient_info()
    return {"symptoms": symptoms, **info}

def collect_from_mobile():
    """
    Collect data from mobile reports via user input.
    Returns a dictionary of symptom counts and patient info.
    """
    symptoms = {}
    print("Enter mobile report data (leave blank to skip a symptom):")
    fever = input("Number of fever cases: ")
    cough = input("Number of cough cases: ")
    if fever.isdigit():
        symptoms["fever"] = int(fever)
    if cough.isdigit():
        symptoms["cough"] = int(cough)
    info = collect_patient_info()
    return {"symptoms": symptoms, **info}

def collect_from_sensors():
    """
    Simulate collecting data from sensors (could be replaced with IoT device integration).
    Returns a dictionary of sensor readings.
    """
    # Example: Replace with real data collection logic
    return {"temperature": 37.8, "humidity": 60}

if __name__ == "__main__":
    # Example usage
    print("Clinic data:", collect_from_clinic())
    print("Mobile data:", collect_from_mobile())
    print("Sensor data:", collect_from_sensors())
