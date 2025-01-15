

import streamlit as st

# Function to display home page with buttons
def home_page():
    st.markdown("""
            <style>
        .stApp {
        background: linear-gradient(to right, #FFFACD, #FFEB3B); /* Soft yellow to golden yellow gradient */
    }
        body {
            font-family: 'Georgia', serif;
            background-color: #FFEB3B; /* Yellow background */
            margin: 0;
            padding: 0;
            color: black; /* Black text color */
        }
        .container {
            text-align: center;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            padding: 50px;
            width: 60%;
            max-width: 600px;
            margin: 10% auto;
        }
        h1 {
            font-size: 48px;
            color: black; /* Black text for header */
            margin-bottom: 30px;
            font-weight: bold;
        }
        h2 {
            font-size: 32px;
            color: black; /* Black text for subheading */
            margin-bottom: 40px;
            font-style: italic;
        }
        .btn-container {
            display: flex;
            justify-content: center;
            gap: 20px; /* Space between buttons */
            flex-wrap: wrap;
        }
        .stButton>button {
            background-color: #673AB7; /* Button color changed to purple */
            color: white !important; /* Force text color to white */
            padding: 20px 40px;
            font-size: 22px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            width: 200px;
            text-align: center;
            text-decoration: none; /* Remove underline */
        }
        .stButton>button:hover {
            background-color: #5e35b1;
            transform: scale(1.05);
        }
        .stButton>button:active {
            background-color: #512da8;
            transform: scale(1);
        }
        .footer {
            position: absolute;
            bottom: 20px;
            width: 100%;
            text-align: center;
            font-size: 16px;
            color: black; /* Footer text in black */
        }
    </style>
    """, unsafe_allow_html=True)


    # Main content of the page
    with st.container():
        st.markdown(
    """
    <h1 style="font-size: 3em; text-align: center; color: black;">
        <i class="fas fa-sun"></i> <span style="color: black; font-weight: bold;">🎓RiseNShine</span>
    </h1>
    <h3 style="text-align: center; color: black;">Your Personalized Educational Assistant</h3>
    """,
    unsafe_allow_html=True
    )


    # Container for buttons
    with st.container():
        col1, col2, col3 = st.columns(3)  # Create 3 columns for better button alignment

        with col1:
            if st.button('Doubt Clarifier'):
                st.session_state.page = "doubt_clarifier"  # Set page flag
        with col2:
            if st.button('Pomo Focus'):
                st.session_state.page = "focus_room"  # Set page flag
        with col3:
            if st.button('Quiz'):
                st.session_state.page = "quiz"  # Set page flag

    # Footer section
    with st.container():
        st.markdown("""
            <div style="text-align: center; padding: 20px; font-size: 14px;">
                <p>&copy; 2025 RiseNShine. All Rights Reserved.</p>
            </div>
        """, unsafe_allow_html=True)


# Main execution
if __name__ == '__main__':
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()  # Display home page
    elif st.session_state.page == "doubt_clarifier":
        import page_1  # Import page_1 from a separate file
        page_1.run()  # Run the function from page_1
    elif st.session_state.page == 'focus_room':
        import pomodoro as pomodoro 
        pomodoro.run()

    elif st.session_state.page == 'quiz':
        import quiz as quiz 
        quiz.run()