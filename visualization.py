# visualization.py
"""
Module for visualizing health data trends and outbreaks.
"""
import matplotlib.pyplot as plt

def plot_total_cases(total_cases):
    plt.bar(['Cases'], [total_cases])
    plt.title('Total Reported Cases')
    plt.ylabel('Number of Cases')
    plt.show()

if __name__ == "__main__":
    from data_analysis import analyze_reports
    from data_storage import get_reports
    reports = get_reports()
    result = analyze_reports(reports)
    plot_total_cases(result["total_cases"])
