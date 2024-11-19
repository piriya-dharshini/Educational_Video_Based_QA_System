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

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

# Set up the Streamlit app
st.set_page_config(page_title="Text Analysis Dashboard", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
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

# Create the layout with 2 rows and 3 columns
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

# First Row: Coarse Label Frequency, Fine Label Frequency, Word Cloud
with row1_col1:
    st.subheader("Coarse Label Frequency")
    coarse_freq = df['label-coarse'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    coarse_freq.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row1_col2:
    st.subheader("Fine Label Frequency")
    fine_freq = df['label-fine'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    fine_freq.plot(kind='bar', color='lightgreen', edgecolor='black', ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row1_col3:
    st.subheader("Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Second Row: Most Common Words, Word Frequency Distribution, Distribution of Word Length
with row2_col1:
    st.subheader("Top 10 Most Common Words")
    most_common = word_freq.most_common(10)
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    ax.bar(*zip(*most_common), color="pink")
    ax.set_xticklabels([item[0] for item in most_common], rotation=45)
    ax.set_xlabel('Words')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with row2_col2:
    st.subheader("Word Frequency Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    sns.histplot(word_freq.values(), bins=30, kde=True, ax=ax)
    ax.set_xlabel('Word Frequency')
    ax.set_ylabel('Count')
    st.pyplot(fig)

with row2_col3:
    st.subheader("Distribution of Word Lengths")
    word_lengths = [len(word) for word in words]
    fig, ax = plt.subplots(figsize=(8, 5))  # Reduced size
    ax.hist(word_lengths, bins=20, color='darkslategray', edgecolor='k')
    ax.set_xlabel('Word Length')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Word Lengths')
    st.pyplot(fig)
