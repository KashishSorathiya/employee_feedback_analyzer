import os
import pandas as pd
import random
import os

def generate_dummy_feedback(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # auto-create folder
    employees = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
    departments = ["HR", "IT", "Finance", "Marketing", "Operations"]
    # Positive feedback messages with more varied keywords
    positive_feedbacks = [
        "Great work environment and supportive team!",
        "Excellent benefits and compensation package",
        "Love the collaborative atmosphere",
        "Amazing mentorship program",
        "Good growth opportunities and learning culture",
        "Fantastic leadership and clear direction",
        "Wonderful colleagues and team spirit",
        "Impressive training and development programs",
        "Flexible working hours and good work-life balance",
        "Innovative projects and cutting-edge technology",
        "Transparent communication from management",
        "Rewarding recognition for achievements",
        "Inclusive workplace culture and diversity",
        "Competitive salary and bonus structure",
        "Excellent health benefits and wellness programs"
    ]
    
    # Negative feedback messages with more varied keywords
    negative_feedbacks = [
        "Extremely dissatisfied with management decisions",
        "Poor work-life balance and long hours",
        "Communication needs significant improvement",
        "Frustrated with outdated technology",
        "Limited career advancement opportunities",
        "Toxic workplace environment and office politics",
        "Inadequate compensation for the workload",
        "Micromanagement is hampering productivity",
        "Lack of recognition for hard work",
        "Insufficient training for new technologies",
        "Stressful deadlines and unrealistic expectations",
        "Poor leadership and unclear direction",
        "Unfair performance evaluation process",
        "Disorganized project management",
        "High turnover rate affecting team morale"
    ]
    
    # Neutral feedback messages
    neutral_feedbacks = [
        "Average workplace with standard benefits",
        "Some processes need improvement",
        "Mixed experiences with different teams",
        "Decent work environment but nothing exceptional",
        "Acceptable compensation but room for improvement",
        "Moderate growth opportunities",
        "Standard training programs",
        "Reasonable workload most of the time",
        "Adequate communication channels",
        "Satisfactory management practices"
    ]
    
    # Combine all feedback types
    feedbacks = positive_feedbacks + negative_feedbacks + neutral_feedbacks

    data = []
    for _ in range(50):
        data.append({
            "Employee": random.choice(employees),
            "Department": random.choice(departments),
            "Feedback": random.choice(feedbacks),
            "Rating": random.randint(1, 5)
        })

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Dummy feedback generated at {file_path}")

if __name__ == "__main__":
    generate_dummy_feedback("data/feedback.csv")
