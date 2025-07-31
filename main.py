import os
import argparse
from datetime import datetime
from src.data_generation import generate_dummy_feedback
from src.report_generator import save_reports
from src.sentiment_analyzer import add_sentiment_to_feedback
from src.analyzer import analyze_feedback


def main(versioned=False, department=None):
    # Paths
    data_dir = "data"
    reports_dir = "reports"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    feedback_file = os.path.join(data_dir, "feedback.csv")
    sentiment_file = os.path.join(data_dir, "feedback_with_sentiment.csv")

    # Ask department interactively if not provided
    if not department:
        import pandas as pd
        df = pd.read_csv(feedback_file)
        departments = df["Department"].unique().tolist()
        print("\nAvailable Departments:")
        for i, dept in enumerate(departments, start=1):
            print(f"{i}. {dept}")
        choice = input("Select department by number (or press Enter for All): ")
        if choice.strip().isdigit():
            department = departments[int(choice) - 1]
        else:
            department = None

    # Versioning
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") if versioned else ""
    suffix = f"_{timestamp}" if versioned else ""

    json_report = os.path.join(reports_dir, f"feedback_summary{suffix}.json")
    csv_report = os.path.join(reports_dir, f"feedback_summary{suffix}.csv")
    chart_report = os.path.join(reports_dir, f"feedback_summary{suffix}.png")

    # Step 1: Generate Feedback
    print("Generating feedback data...")
    generate_dummy_feedback(feedback_file)

    # Step 2: Perform Sentiment Analysis
    print("Performing sentiment analysis...")
    feedback_file_with_sentiment = os.path.join(data_dir, "feedback_with_sentiment.csv")
    add_sentiment_to_feedback(feedback_file, feedback_file_with_sentiment)

    # Step 3: Save Reports
    print("Saving reports...")
    save_reports(feedback_file_with_sentiment, reports_dir)
    print(f"\nReports generated at: {reports_dir}\n")
    
    # Remove or comment out these redundant lines
    # Step 4: Save Reports
    # print("Saving reports...")
    # save_reports(sentiment_file, reports_dir)
    # save_reports("data/feedback.csv", "reports")
    # print(f"\nReports generated at: {reports_dir}\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Employee Feedback Analyzer")
    parser.add_argument("--versioned", action="store_true", help="Save reports with timestamp")
    parser.add_argument("--department", type=str, help="Filter reports by department")
    args = parser.parse_args()
    main(versioned=args.versioned, department=args.department)
