import streamlit as st
import data_storage
import pandas as pd
import os
from datetime import date
import random
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_db():
    if not os.path.exists('health_data.db'):
        data_storage.init_db()

def get_data():
    reports = data_storage.get_reports()
    columns = [
        "case_id", "report_date", "location", "disease_name", "symptoms", "diagnosis_status",
        "patient_age", "patient_sex", "health_facility", "report_source"
    ]
    data = [dict(zip(columns, r)) for r in reports]
    return pd.DataFrame(data)

def data_entry_page():
    st.markdown("""
        <style>
        body, .stApp { background: #f8f9fa; color: #222; }
        .modern-form {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px #e0e0e0;
            padding: 2.5em 2em 2em 2em;
            max-width: 520px;
            margin: 2em auto 2em auto;
        }
        .modern-form label {
            font-weight: 600;
            color: #34495e;
            margin-bottom: 0.3em;
            position: relative;
            display: block;
            transition: color 0.2s;
        }
        .modern-form input, .modern-form select, .modern-form textarea {
            width: 100%;
            padding: 1.2em 0.7em 0.5em 0.7em;
            margin-bottom: 1.5em;
            border-radius: 8px;
            border: 1px solid #dfe6e9;
            background: #fff;
            color: #222;
            font-size: 1em;
            transition: border 0.2s, background 0.2s;
        }
        .modern-form input:focus, .modern-form select:focus, .modern-form textarea:focus {
            border: 1.5px solid #0984e3;
            background: #fff;
            outline: none;
        }
        .modern-form .floating-label {
            position: absolute;
            left: 0.8em;
            top: 1.2em;
            color: #636e72;
            pointer-events: none;
            transition: 0.2s;
            font-size: 1em;
        }
        .modern-form input:focus + .floating-label,
        .modern-form input:not(:placeholder-shown) + .floating-label,
        .modern-form textarea:focus + .floating-label,
        .modern-form textarea:not(:placeholder-shown) + .floating-label {
            top: -0.7em;
            left: 0.5em;
            font-size: 0.85em;
            color: #0984e3;
            background: #fff;
            padding: 0 0.3em;
        }
        .modern-form button {
            background: linear-gradient(90deg, #0984e3 0%, #00b894 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.9em 2.2em;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 8px #e0e0e0;
            transition: background 0.2s, transform 0.2s;
            position: relative;
            overflow: hidden;
        }
        .modern-form button:active {
            transform: scale(0.97);
        }
        .modern-form button.loading::after {
            content: '';
            position: absolute;
            left: 50%;
            top: 50%;
            width: 22px;
            height: 22px;
            border: 3px solid #fff;
            border-top: 3px solid #0984e3;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            transform: translate(-50%, -50%);
        }
        @keyframes spin {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        @media (max-width: 600px) {
            .modern-form { max-width: 98vw; padding: 1.2em 0.5em; }
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="modern-form">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#00b894; margin-bottom:1.5em;">Submit New Disease Case Report</h2>', unsafe_allow_html=True)
    with st.form("report_form"):
        case_id = st.text_input('', key='case_id', placeholder=' ', help='Unique identifier for this report')
        st.markdown('<label class="floating-label" for="case_id">Case ID</label>', unsafe_allow_html=True)
        report_date = st.date_input('', key='report_date', help='Date of symptom onset or reporting')
        st.markdown('<label class="floating-label" for="report_date">Report Date</label>', unsafe_allow_html=True)
        location = st.text_input('', key='location', placeholder=' ', help='Enter the region, LGA, or GPS coordinates')
        st.markdown('<label class="floating-label" for="location">Location (LGA/Region/GPS)</label>', unsafe_allow_html=True)
        disease_name = st.text_input('', key='disease_name', placeholder=' ', help='Name of suspected/confirmed disease')
        st.markdown('<label class="floating-label" for="disease_name">Disease Name</label>', unsafe_allow_html=True)
        symptoms = st.text_area('', key='symptoms', placeholder=' ', help='e.g. fever, cough, diarrhea')
        st.markdown('<label class="floating-label" for="symptoms">Symptoms (comma-separated)</label>', unsafe_allow_html=True)
        diagnosis_status = st.selectbox('Diagnosis Status', ['Suspected', 'Confirmed', 'Ruled Out'], help='Status of diagnosis')
        patient_age = st.number_input('Patient Age', min_value=0, max_value=120, step=1, help='Age of the patient')
        patient_sex = st.selectbox('Patient Sex', ['Male', 'Female', 'Other'], help='Sex of the patient')
        health_facility = st.text_input('', key='health_facility', placeholder=' ', help='Reporting clinic or hospital')
        st.markdown('<label class="floating-label" for="health_facility">Health Facility (Name/ID)</label>', unsafe_allow_html=True)
        report_source = st.selectbox('Report Source', ['Community Agent', 'SMS', 'Clinic App', 'IoT Device', 'Web Portal', 'Mobile App', 'Other'], help='How was this report submitted?')
        submitted = st.form_submit_button('Submit', help='Submit this case report')
        if submitted:
            st.markdown('<script>document.querySelector("button[type=submit]").classList.add("loading");</script>', unsafe_allow_html=True)
            data_storage.store_report(
                case_id=case_id,
                report_date=str(report_date),
                location=location,
                disease_name=disease_name,
                symptoms=symptoms,
                diagnosis_status=diagnosis_status,
                patient_age=patient_age,
                patient_sex=patient_sex,
                health_facility=health_facility,
                report_source=report_source
            )
            st.success('Case report submitted!')
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    st.markdown("""
        <style>
        .dashboard-title {font-size:2.2rem; font-weight:700; color:#2c3e50; margin-bottom:0.5em;}
        .dashboard-section {background:#f8f9fa; border-radius:16px; padding:1.5em; margin-bottom:1.5em; box-shadow:0 4px 16px #e0e0e0;}
        .dashboard-subtitle {font-size:1.2rem; font-weight:600; color:#34495e; margin-bottom:0.7em;}
        .stDataFrame {background: #fff !important; border-radius: 8px;}
        .chart-card {background: #fff; border-radius: 14px; box-shadow: 0 2px 8px #e0e0e0; padding: 1em; margin-bottom: 1.5em;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="dashboard-title">📊 Disease Surveillance Dashboard</div>', unsafe_allow_html=True)
    df = get_data()
    chart_types = ['bar', 'line', 'area', 'pie']
    palette_list = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Dark2', 'Accent', 'tab10', 'tab20']
    def random_chart_type():
        return random.choice(chart_types)
    def random_palette():
        return random.choice(palette_list)
    if not df.empty:
        with st.container():
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">All Reports</div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        # Chart 1: Cases by Disease Name
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Cases by Disease Name</div>', unsafe_allow_html=True)
            disease_counts = df['disease_name'].value_counts()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                disease_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(disease_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=disease_counts.index, y=disease_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Disease')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=disease_counts.index, y=disease_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Disease')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(disease_counts.index, disease_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(disease_counts.index, disease_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Disease')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
        # Chart 2: Cases by Patient Age
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Cases by Patient Age</div>', unsafe_allow_html=True)
            age_counts = df['patient_age'].value_counts().sort_index()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                age_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(age_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=age_counts.index, y=age_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Age')
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=age_counts.index, y=age_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Age')
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(age_counts.index, age_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(age_counts.index, age_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Age')
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
        # Chart 3: Cases by Patient Sex
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Cases by Patient Sex</div>', unsafe_allow_html=True)
            sex_counts = df['patient_sex'].value_counts()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                sex_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(sex_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=sex_counts.index, y=sex_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Sex')
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=sex_counts.index, y=sex_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Sex')
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(sex_counts.index, sex_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(sex_counts.index, sex_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Sex')
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
        # Chart 4: Cases by Location
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Cases by Location</div>', unsafe_allow_html=True)
            loc_counts = df['location'].value_counts()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                loc_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(loc_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=loc_counts.index, y=loc_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Location')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=loc_counts.index, y=loc_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Location')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(loc_counts.index, loc_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(loc_counts.index, loc_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Location')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
        # Chart 5: Diagnosis Status Distribution
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Diagnosis Status Distribution</div>', unsafe_allow_html=True)
            diag_counts = df['diagnosis_status'].value_counts()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                diag_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(diag_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=diag_counts.index, y=diag_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Diagnosis Status')
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=diag_counts.index, y=diag_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Diagnosis Status')
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(diag_counts.index, diag_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(diag_counts.index, diag_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Diagnosis Status')
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
        # Chart 6: Cases by Report Source
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-subtitle">Cases by Report Source</div>', unsafe_allow_html=True)
            src_counts = df['report_source'].value_counts()
            chart_type = random_chart_type()
            palette = random_palette()
            if chart_type == 'pie':
                fig, ax = plt.subplots()
                src_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette(palette, len(src_counts)), ax=ax, ylabel='')
                st.pyplot(fig)
            elif chart_type == 'bar':
                fig, ax = plt.subplots()
                sns.barplot(x=src_counts.index, y=src_counts.values, palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Report Source')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'line':
                fig, ax = plt.subplots()
                sns.lineplot(x=src_counts.index, y=src_counts.values, marker='o', palette=palette, ax=ax)
                ax.set_ylabel('Cases')
                ax.set_xlabel('Report Source')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            elif chart_type == 'area':
                fig, ax = plt.subplots()
                ax.fill_between(src_counts.index, src_counts.values, color=sns.color_palette(palette)[0], alpha=0.5)
                ax.plot(src_counts.index, src_counts.values, color=sns.color_palette(palette)[1])
                ax.set_ylabel('Cases')
                ax.set_xlabel('Report Source')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            st.caption(f"Chart type: {chart_type.title()} | Palette: {palette}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info('No data to display yet.')

def csv_batch_import_page():
    st.markdown("""
        <style>
        .csv-upload-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px #e0e0e0;
            padding: 2.5em 2em 2em 2em;
            max-width: 520px;
            margin: 2em auto 2em auto;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="csv-upload-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#0984e3; margin-bottom:1.5em;">Batch Import Disease Reports (CSV)</h2>', unsafe_allow_html=True)
    st.info("Download the sample CSV below to see the required format. Your file must have these columns:")
    # Show sample data
    import pandas as pd
    sample_df = pd.read_csv('sample_disease_surveillance_data.csv')
    st.dataframe(sample_df.head(5), use_container_width=True, hide_index=True)
    st.download_button(
        label="Download Sample CSV",
        data=sample_df.to_csv(index=False),
        file_name="sample_disease_surveillance_data.csv",
        mime="text/csv"
    )
    uploaded_file = st.file_uploader("Choose a CSV file to import", type=["csv"])
    if uploaded_file is not None:
        try:
            # Save uploaded file to a temp location
            temp_path = "temp_uploaded_data.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            data_storage.import_from_csv(temp_path)
            st.success("CSV data imported successfully!")
            os.remove(temp_path)
        except Exception as e:
            st.error(f"Error importing CSV: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title('Real-Time Local Disease Surveillance and Reporting System')
    ensure_db()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Dashboard", "Data Entry", "Batch CSV Import"))
    if page == "Dashboard":
        dashboard_page()
    elif page == "Data Entry":
        data_entry_page()
    elif page == "Batch CSV Import":
        csv_batch_import_page()

if __name__ == "__main__":
    main()
