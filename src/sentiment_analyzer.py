from textblob import TextBlob
import pandas as pd

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def add_sentiment_to_feedback(input_file, output_file):
    df = pd.read_csv(input_file)
    df["Sentiment"] = df["Feedback"].apply(analyze_sentiment)
    df.to_csv(output_file, index=False)
    print(f"Sentiment analysis added and saved to {output_file}")

if __name__ == "__main__":
    add_sentiment_to_feedback("data/feedback.csv", "data/feedback_with_sentiment.csv")
