import streamlit as st
import pandas as pd
import random

# Function to load the quiz questions from a CSV file
def load_questions(csv_file):
    return pd.read_csv(csv_file)

# Function to run the quiz
def run_quiz(questions_df):
    score = 0
    total_questions = len(questions_df)
    selected_questions = questions_df.sample(frac=1).reset_index(drop=True)

    for idx, row in selected_questions.iterrows():
        st.write(f"### Question {idx + 1}: {row['Question']}")

        options = [row['Option1'], row['Option2'], row['Option3'], row['Option4']]
        random.shuffle(options)

        selected_option = st.radio("Select an option:", options, key=f"question_{idx}")

        if st.button(f"Submit Answer for Question {idx + 1}", key=f"submit_{idx}"):
            if selected_option == row['CorrectAnswer']:
                st.success("Correct Answer!")
                score += 1
            else:
                st.error(f"Wrong Answer! The correct answer is: {row['CorrectAnswer']}")

    st.write("## Quiz Completed!")
    st.write(f"Your Score: {score} / {total_questions}")

# Streamlit application
st.title("Quiz Tool with Streamlit")

uploaded_file = st.file_uploader("Upload a CSV file with quiz questions", type=["csv"])

if uploaded_file is not None:
    questions_df = load_questions(uploaded_file)
    run_quiz(questions_df)
else:
    st.write("Please upload a CSV file to start the quiz.")
