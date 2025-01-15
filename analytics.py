import streamlit as st
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from collections import Counter
import seaborn as sns
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import pickle
# Download necessary NLTK resources
nltk.download('punkt')
# Function to classify the question's label
def classify_question(question):
    # Labels mapping
    labels = {
        0: "Description",
        1: "Numeric (Phrased Descriptively)",
        2: "Abbreviation",
        3: "Human",
        4: "Actual Numerical Values",
        5: "Location"
    }

    # Load the pre-trained vectorizer and model (ensure these are saved in the correct location)
    try:
        with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        with open('model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)

        # Vectorize the question
        question_vec = vectorizer.transform([question])

        # Predict the label
        predicted_label = model.predict(question_vec)

        # Map the predicted label to its corresponding description
        label_description = labels.get(predicted_label[0], "Unknown label")
        return label_description
    except Exception as e:
        return f"Error: {str(e)}"

# Set up the Streamlit app
st.set_page_config(page_title="Text Analysis Dashboard", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #000000; /* Black background */
    }
    .metric-card {
        background: #ffffff; /* White card background for contrast */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# Load the dataset (replace with your path)
df = pd.read_csv('train.csv')  # Update the path as needed

# Tokenize the text column
text = ' '.join(df['text'])
words = word_tokenize(text.lower())

# Filter out common words
common_words = {',', '.', 'a', 'that', 'this', 'is', 'and', 'the', 'to', 'it', 'of', '\'s', 'so', '?'}
filtered_words = [word for word in words if word not in common_words]

# Calculate word frequencies
word_freq = Counter(filtered_words)

# Create the layout with 4 rows
row1_col1, row1_col2, row1_col3 = st.columns(3)  # Row 1: Summary Metrics
row2_col1, row2_col2 = st.columns(2)             # Row 2: Question and Answer
row3_col1, row3_col2, row3_col3 = st.columns(3)  # Row 3: Label Frequencies and Word Cloud
row4_col1, row4_col2, row4_col3 = st.columns(3)  # Row 4: Other Visualizations

# First Row: Summary Metrics
with row1_col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Label-Fine")
    st.metric(label="Count", value="5")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Label-Coarse")
    st.metric(label="Count", value="46")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Total Samples")
    st.metric(label="Count", value="5453")
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col1:
    st.subheader("Enter Question")
    question = st.text_input("Type your question here:")

    # Show the question entered
    if question:
        st.write(f"Your Question: {question}")

with row2_col2:
    st.subheader("Prediction")
    if question:
        # Call the classify_question function
        classification_result = classify_question(question)
        st.write(f"Predicted Label: {classification_result}")
# Third Row: Coarse Label Frequency, Fine Label Frequency, Word Cloud
with row3_col1:
    st.subheader("Coarse Label Frequency")
    coarse_freq = df['label-coarse'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    coarse_freq.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row3_col2:
    st.subheader("Fine Label Frequency")
    fine_freq = df['label-fine'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    fine_freq.plot(kind='bar', color='lightgreen', edgecolor='black', ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row3_col3:
    st.subheader("Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Fourth Row: Most Common Words, Word Frequency Distribution, Distribution of Word Length
with row4_col1:
    st.subheader("Top 10 Most Common Words")
    most_common = word_freq.most_common(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(*zip(*most_common), color="pink")
    ax.set_xticklabels([item[0] for item in most_common], rotation=45)
    ax.set_xlabel('Words')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row4_col2:
    st.subheader("Word Frequency Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(word_freq.values(), bins=30, kde=True, ax=ax)
    ax.set_xlabel('Word Frequency')
    ax.set_ylabel('Count')
    st.pyplot(fig)

with row4_col3:
    st.subheader("Distribution of Word Lengths")
    word_lengths = [len(word) for word in words]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(word_lengths, bins=20, color='darkslategray', edgecolor='k')
    ax.set_xlabel('Word Length')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Word Lengths')
    st.pyplot(fig)
