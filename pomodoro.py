import streamlit as st
import time

# Function to display the work screen (Pomodoro timer with countdown)
def display_work_screen(remaining_time, timer_placeholder):
    # Applying gradient background for work screen
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #B3A7D3, #FFB6B9); /* Soft lavender to light peach gradient */
        }
        </style>
        """, unsafe_allow_html=True
    )

    timer_placeholder.markdown(
        f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; height: 100vh; text-align: center;'>
            <div style='font-size: 48px; margin-bottom: 20px;'>
                <span role="img" aria-label="focus" style="font-size: 60px;">📚</span>
                <h1>PomoFocus</h1>
            </div>
            <div style='background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);'>
                <h1 style='font-size: 48px; color: #333;'>Work Time: {remaining_time // 60}:{remaining_time % 60:02d}</h1>
            </div>
        </div>
        """, unsafe_allow_html=True
    )


# Function to display break screen (Break timer with countdown)
def display_break_screen(remaining_time, timer_placeholder):
    # Applying gradient background for break screen
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #A7D8D8, #B4F8C8);  /* Soft blue to mint green gradient */
        }
        </style>
        """, unsafe_allow_html=True
    )

    timer_placeholder.markdown(
        f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; height: 100vh; text-align: center;'>
            <div style='font-size: 48px; margin-bottom: 20px;'>
                <span role="img" aria-label="break" style="font-size: 60px;">🌴</span>
                <h1>Take Break</h1>
            </div>
            <div style='background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);'>
                <h1 style='font-size: 48px; color: #333;'>Break Time: {remaining_time // 60}:{remaining_time % 60:02d}</h1>
            </div>
        </div>
        """, unsafe_allow_html=True
    )


# Main script
if 'pomodoro_running' not in st.session_state:
    st.session_state.pomodoro_running = False

if 'cycle_count' not in st.session_state:
    st.session_state.cycle_count = 0

# Function to start the Pomodoro timer
def start_pomodoro():
    st.session_state.pomodoro_running = True
    work_time = 1 * 60  # 25 minutes for work time
    break_time = 1 * 60  # 5 minutes for break time

    timer_placeholder = st.empty()  # Create an empty placeholder for the timer

    while st.session_state.pomodoro_running:
        # Work time: 25 minutes countdown
        for t in range(work_time, 0, -1):
            if not st.session_state.pomodoro_running:
                break
            display_work_screen(t, timer_placeholder)
            time.sleep(1)  # Wait for 1 second

        if not st.session_state.pomodoro_running:
            break

        # Break time: 5 minutes countdown
        for t in range(break_time, 0, -1):
            if not st.session_state.pomodoro_running:
                break
            display_break_screen(t, timer_placeholder)
            time.sleep(1)  # Wait for 1 second

        if not st.session_state.pomodoro_running:
            break

        st.session_state.cycle_count += 1
        if st.session_state.cycle_count >= 4:
            break


# Button to start or stop the Pomodoro timer
if not st.session_state.pomodoro_running:
    start_pomodoro()
