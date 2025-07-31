import pandas as pd
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

def extract_keywords(texts, sentiment_filter=None, top_n=5):
    """
    Extract most common words from feedback texts, optionally filtered by sentiment.
    """
    # Combine all texts into one string
    all_text = " ".join(texts).lower()
    
    # Remove special characters and numbers
    all_text = re.sub(r'[^a-zA-Z\s]', '', all_text)
    
    # Split into words
    words = all_text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Return top N words
    return dict(word_counts.most_common(top_n))

def analyze_feedback(file_path, department=None):
    """
    Analyze employee feedback data for ratings and sentiments.
    Optionally filter by department.
    """
    # Load feedback CSV
    df = pd.read_csv(file_path)

    # If filtering by department
    if department and department in df["Department"].unique():
        df = df[df["Department"] == department]

    # Average rating
    avg_rating = df["Rating"].mean()

    # Rating distribution
    rating_distribution = df["Rating"].value_counts().to_dict()

    # Sentiment distribution
    sentiment_distribution = df["Sentiment"].value_counts().to_dict()

    # Department-wise sentiment distribution
    department_sentiment = (
        df.groupby("Department")["Sentiment"]
        .value_counts()
        .unstack(fill_value=0)
        .to_dict()
    )
    
    # Department-wise ratings
    department_ratings = df.groupby("Department")["Rating"].agg(['mean', 'min', 'max', 'count']).to_dict()
    
    # Extract top keywords by sentiment
    positive_keywords = extract_keywords(df[df["Sentiment"] == "Positive"]["Feedback"].tolist())
    negative_keywords = extract_keywords(df[df["Sentiment"] == "Negative"]["Feedback"].tolist())
    neutral_keywords = extract_keywords(df[df["Sentiment"] == "Neutral"]["Feedback"].tolist())
    
    # Department-wise keywords
    department_keywords = {}
    for dept in df["Department"].unique():
        dept_df = df[df["Department"] == dept]
        department_keywords[dept] = {
            "positive": extract_keywords(dept_df[dept_df["Sentiment"] == "Positive"]["Feedback"].tolist(), top_n=3),
            "negative": extract_keywords(dept_df[dept_df["Sentiment"] == "Negative"]["Feedback"].tolist(), top_n=3)
        }

    # Return summary
    return {
        "average_rating": avg_rating,
        "rating_distribution": rating_distribution,
        "sentiment_distribution": sentiment_distribution,
        "department_sentiment": department_sentiment,
        "department_ratings": department_ratings,
        "keywords": {
            "positive": positive_keywords,
            "negative": negative_keywords,
            "neutral": neutral_keywords
        },
        "department_keywords": department_keywords
    }
