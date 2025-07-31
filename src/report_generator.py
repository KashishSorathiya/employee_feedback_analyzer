import json
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .analyzer import analyze_feedback

def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def save_csv(data, file_path):
    with open(file_path, "w", newline='') as f:
        writer = csv.writer(f)
        for key, value in data.items():
            writer.writerow([key, value])

def save_bar_chart(data, file_path, xlabel, ylabel, title, color='skyblue', horizontal=False, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    if horizontal:
        plt.barh(list(data.keys()), list(data.values()), color=color)
        plt.xlabel(ylabel)
        plt.ylabel(xlabel)
    else:
        plt.bar(data.keys(), data.values(), color=color)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

def department_wise_chart(file_path, chart_path):
    df = pd.read_csv(file_path)
    dept_ratings = df.groupby("Department")["Rating"].mean().to_dict()
    save_bar_chart(dept_ratings, chart_path, "Department", "Average Rating", "Department-wise Average Rating")

def save_reports(feedback_file, report_folder):
    summary = analyze_feedback(feedback_file)
    save_json(summary, f"{report_folder}/summary.json")
    save_csv(summary["rating_distribution"], f"{report_folder}/summary.csv")
    
    # Basic charts
    save_bar_chart(summary["rating_distribution"], f"{report_folder}/rating_distribution.png", "Ratings", "Count", "Rating Distribution")
    department_wise_chart(feedback_file, f"{report_folder}/department_wise_ratings.png")
    sentiment_distribution_chart(feedback_file, f"{report_folder}/sentiment_distribution.png")
    department_sentiment_chart(summary["department_sentiment"], f"{report_folder}/department_sentiment.png")
    
    # New advanced charts
    keyword_charts(summary["keywords"], report_folder)
    department_insights_chart(summary["department_ratings"], summary["department_sentiment"], report_folder)
    department_keywords_chart(summary["department_keywords"], report_folder)
    
    print(f"\nReports generated successfully in '{report_folder}' folder.")

def sentiment_distribution_chart(file_path, chart_path):
    df = pd.read_csv(file_path)
    sentiment_counts = df["Sentiment"].value_counts().to_dict()
    
    # Create a pie chart for sentiment distribution
    plt.figure(figsize=(8, 8))
    colors = {"Positive": "green", "Neutral": "gray", "Negative": "red"}
    plt.pie(
        sentiment_counts.values(), 
        labels=sentiment_counts.keys(),
        autopct='%1.1f%%',
        colors=[colors.get(s, 'blue') for s in sentiment_counts.keys()],
        startangle=90,
        shadow=True
    )
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title("Sentiment Distribution")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    
    # Also create a bar chart version
    save_bar_chart(sentiment_counts, f"{chart_path.replace('.png', '_bar.png')}", 
                  "Sentiment", "Count", "Sentiment Distribution",
                  color=[colors.get(s, 'blue') for s in sentiment_counts.keys()])

def department_sentiment_chart(data, file_path):
    departments = list(data.keys())
    sentiments = ["Positive", "Neutral", "Negative"]

    # Get counts for each sentiment
    counts = {s: [data[dept].get(s, 0) for dept in departments] for s in sentiments}

    # Plot stacked bars
    plt.figure(figsize=(12, 7))
    bottom = np.zeros(len(departments))
    colors = {"Positive": "green", "Neutral": "gray", "Negative": "red"}
    for sentiment in sentiments:
        plt.bar(departments, counts[sentiment], bottom=bottom, label=sentiment, color=colors[sentiment])
        bottom += counts[sentiment]

    plt.xlabel("Department")
    plt.ylabel("Number of Feedbacks")
    plt.title("Department-wise Sentiment Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

def keyword_charts(keywords_data, report_folder):
    # Create horizontal bar charts for keywords by sentiment
    for sentiment, keywords in keywords_data.items():
        if keywords:  # Only create chart if there are keywords
            colors = {"positive": "green", "negative": "red", "neutral": "gray"}
            save_bar_chart(
                keywords, 
                f"{report_folder}/{sentiment}_keywords.png", 
                "Keywords", "Frequency", 
                f"Top Keywords in {sentiment.capitalize()} Feedback",
                color=colors.get(sentiment.lower(), 'blue'),
                horizontal=True,
                figsize=(10, 6)
            )

def department_insights_chart(dept_ratings, dept_sentiment, report_folder):
    # Create a comprehensive department insights chart
    departments = list(dept_ratings['mean'].keys())
    
    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1.5]})
    
    # Plot average ratings
    avg_ratings = [dept_ratings['mean'][dept] for dept in departments]
    bars = ax1.bar(departments, avg_ratings, color='skyblue')
    ax1.set_ylabel('Average Rating')
    ax1.set_title('Department Performance Overview')
    
    # Add rating values on top of bars
    for bar, rating in zip(bars, avg_ratings):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{rating:.2f}', ha='center', va='bottom')
    
    # Plot sentiment distribution as stacked bars
    sentiments = ["Positive", "Neutral", "Negative"]
    bottom = np.zeros(len(departments))
    colors = {"Positive": "green", "Neutral": "gray", "Negative": "red"}
    
    for sentiment in sentiments:
        sentiment_counts = [dept_sentiment.get(dept, {}).get(sentiment, 0) for dept in departments]
        ax2.bar(departments, sentiment_counts, bottom=bottom, label=sentiment, color=colors[sentiment])
        bottom += sentiment_counts
    
    ax2.set_xlabel('Department')
    ax2.set_ylabel('Number of Feedbacks')
    ax2.set_title('Department-wise Sentiment Breakdown')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f"{report_folder}/department_performance_insights.png")
    plt.close()

def department_keywords_chart(dept_keywords, report_folder):
    # Create a chart showing top positive and negative keywords for each department
    departments = list(dept_keywords.keys())
    
    for dept in departments:
        pos_keywords = dept_keywords[dept]['positive']
        neg_keywords = dept_keywords[dept]['negative']
        
        if not pos_keywords and not neg_keywords:
            continue  # Skip if no keywords
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot positive keywords
        if pos_keywords:
            ax1.barh(list(pos_keywords.keys()), list(pos_keywords.values()), color='green')
            ax1.set_xlabel('Frequency')
            ax1.set_title(f'Top Positive Keywords - {dept}')
        else:
            ax1.text(0.5, 0.5, 'No positive keywords found', ha='center', va='center')
            ax1.set_title(f'No Positive Keywords - {dept}')
        
        # Plot negative keywords
        if neg_keywords:
            ax2.barh(list(neg_keywords.keys()), list(neg_keywords.values()), color='red')
            ax2.set_xlabel('Frequency')
            ax2.set_title(f'Top Negative Keywords - {dept}')
        else:
            ax2.text(0.5, 0.5, 'No negative keywords found', ha='center', va='center')
            ax2.set_title(f'No Negative Keywords - {dept}')
        
        plt.tight_layout()
        plt.savefig(f"{report_folder}/{dept}_keywords.png")
        plt.close()

if __name__ == "__main__":
    save_reports("data/feedback.csv", "reports")
