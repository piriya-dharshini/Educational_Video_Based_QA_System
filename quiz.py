import streamlit as st
import requests
import json
import re

def run():

    st.markdown(
            """
            <style>
            .stApp {
        background: linear-gradient(to right, #FFFACD, #FFEB3B); /* Soft yellow to golden yellow gradient */
    }
            </style>
            """, unsafe_allow_html=True
        )

    # Base URL of the FastAPI server
    SERVER_URL = "http://localhost:8000"

    # Initialize session state variables
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "feedback" not in st.session_state:
        st.session_state.feedback = None

    # CSS styling for a neat, classy look
    st.markdown("""
        <style>
            body {
                background-color: #f4f7f6;
                font-family: 'Helvetica Neue', sans-serif;
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
            .stRadio>div>label {
                font-size: 16px;
                color: #333;
            }
            .stSubheader {
                color: #333;
                font-size: 24px;
            }
            .stMetric {
                font-size: 20px;
                font-weight: bold;
            }
            .stText {
                font-size: 18px;
            }
            .stMarkdown {
                font-size: 18px;
                color: #333;
            }
            .success {
                color: #4CAF50;
                font-size: 16px;
            }
            .error {
                color: #f44336;
                font-size: 16px;
            }
            .stSuccess>div, .stError>div {
                background-color: #f9f9f9;
                border-radius: 8px;
                padding: 10px;
            }
            .stMetric>div {
                background-color: #e7f6e7;
                padding: 20px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    @st.fragment
    def load_questions(youtube_url):
        """
        Fetch quiz questions from the server based on the provided YouTube URL.
        """
        response = requests.post(
            f"{SERVER_URL}/generate_quiz_questions", 
            json={"youtube_url": youtube_url}
        )
        if response.status_code == 200:
            data_loaded = response.json()
            data_questions = data_loaded['questions']
            data = data_questions['content']
            # Regular expression to remove code block markers and extract the dictionary part
            pattern = r'```python\nquiz_questions = (\[[\s\S]*?\])\n```'

            # Extract the part containing the list of dictionaries
            match = re.search(pattern, data)
            if match:
                quiz_questions_str = match.group(1)  # Extracted string that represents the list of dicts
                # Use eval to convert the string into the actual Python list of dictionaries
                quiz_questions = eval(quiz_questions_str)
                st.session_state.questions = quiz_questions
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.feedback = None
                st.success("Questions loaded successfully!")
            else:
                st.error("No quiz questions found in the response.")

    @st.fragment
    def question_fragment():
        """
        Fragment to display a question and capture the user's response.
        """
        question_data = st.session_state.questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
        st.write(question_data['question'])

        selected_option = st.radio('Choose an answer: ', question_data['options'])
        if st.button('Submit'):
            if selected_option == question_data['answer']:
                st.session_state.feedback = ('success', 'Correct! 🎉')
                st.session_state.score += 1
            else:
                st.session_state.feedback = ("error", f"Wrong! The correct answer was: {question_data['answer']}")

            if st.session_state.current_question + 1 < len(st.session_state.questions):
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.session_state.current_question = None
                st.rerun()

    @st.fragment
    def feedback_fragment():
        """
        Fragment to display feedback messages.
        """
        if st.session_state.feedback:
            msg_type, msg_content = st.session_state.feedback
            if msg_type == "success":
                st.markdown(f"<div class='success'>{msg_content}</div>", unsafe_allow_html=True)
            elif msg_type == "error":
                st.markdown(f"<div class='error'>{msg_content}</div>", unsafe_allow_html=True)
            st.session_state.feedback = None

    @st.fragment
    def score_fragment():
        """
        Fragment to display the user’s current score.
        """
        st.metric('Current Score', st.session_state.score)

    @st.fragment
    def restart_quiz_fragment():
        """
        Fragment to restart the quiz.
        """
        if st.button('Restart Quiz'):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.feedback = None
            st.session_state.questions = []
            st.rerun()

    # Main application
    st.title('Educational Video Quiz App')

    # Input for YouTube URL
    youtube_url = st.text_input('Enter YouTube URL for Quiz Generation:', placeholder='Paste the YouTube link here...')

    if youtube_url and st.button('Generate Quiz'):
        load_questions(youtube_url)

    feedback_fragment()

    if st.session_state.questions:
        if st.session_state.current_question is not None:
            score_fragment()
            question_fragment()
        else:
            st.subheader('Quiz Finished! 🎉')
            st.write(f"Your final score is {st.session_state.score}/{len(st.session_state.questions)}.")
            restart_quiz_fragment()
    else:
        st.write("Enter a YouTube URL to start the quiz.")
