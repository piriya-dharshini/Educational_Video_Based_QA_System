import streamlit as st
import requests
import os

# Function to extract YouTube video ID from the URL
def get_video_id(url):
    # Check if the URL has a valid format
    if "youtu.be" in url:
        return url.split('/')[-1]
    elif "youtube.com/watch?v=" in url:
        return url.split('v=')[1].split('&')[0]
    elif "youtube.com/embed/" in url:
        return url.split('/')[-1]
    return None

# Set up Streamlit page title and layout
st.set_page_config(page_title="Smart Video Q&A", layout="wide")
st.title("🎓 Smart Video Q&A")
st.subheader("Ask questions about any YouTube video!")

# User inputs
youtube_url = st.text_input("Enter YouTube Video URL:", "")
user_query = st.text_input("What would you like to know?", "")

# Button to submit the question
if st.button("Get Answer"):
    if youtube_url and user_query:
        # Extract video ID and generate thumbnail URL
        video_id = get_video_id(youtube_url)
        if video_id:
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            # Create two columns
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)
            with col2:
                st.write("**Your Question:**", user_query)

                # Sending the YouTube link and question to the FastAPI server
                response = requests.post(
                    "http://localhost:8000/qa",
                    json={'youtube_url': youtube_url, 'input': user_query}
                )
                
                # Display the response
                if response.status_code == 200:
                    response_json = response.json()
                    
                    input_sentence=response_json.get("answer", "No answer found")
                    st.write("**Answer:**", response_json.get("answer", "No answer found"))

                    
                else:
                    st.write("Error:", response.text)
        else:
            st.write("Invalid YouTube URL. Please try again.")
    else:
        st.write("Please enter both a YouTube URL and a question.") 


# Customize the appearance of the Streamlit app with royal colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF9DB; /* Light yellow background */
    }
    body {
        background-color: #FFF9DB; /* Light background */
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4B0082; /* Indigo color */
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #6A0DAD; /* Darker shade of purple on hover */
    }
    .stTextInput>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #6A0DAD; /* Matching border color */
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)