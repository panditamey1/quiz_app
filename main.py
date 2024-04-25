import streamlit as st
import pandas as pd
import random
import os

def load_csvs(folder_path):
    dfs = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def main():
    # Load CSV files from the "csvs" folder
    csvs_folder = "csvs"
    if not os.path.exists(csvs_folder):
        os.makedirs(csvs_folder)
        st.write("Please upload the CSV files to the 'csvs' folder")
    data = load_csvs(csvs_folder)

    # Randomize the order of the rows
    data = data.sample(frac=1).reset_index(drop=True)
    st.title("Quiz App")

    # Initialize session state variables if not already present
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Display the current question
    question_data = data.loc[st.session_state.current_question]
    st.title(question_data['Learning Objective'])
    st.write(question_data['Question'])
    options_dict = {
        question_data["Option A (Correct)"]: "Feedback A",
        question_data["Option B (Incorrect)"]: "Feedback B",
        question_data["Option C (Incorrect)"]: "Feedback C",
    }
    options = list(options_dict.keys())
    random.shuffle(options)

    # Radio buttons for options
    selected_option = st.radio("Choose an answer:", options)

    # Submit button for the answer
    if st.button("Submit Answer"):
        if "Correct" in selected_option:
            st.session_state.score += 1
            st.success("Correct! " + data.loc[st.session_state.current_question, options_dict[selected_option]])
        else:
            correct_option = question_data["Option A (Correct)"]
            st.error(f"Wrong! The correct answer was {correct_option}.\nFeedback: {data.loc[st.session_state.current_question, options_dict[selected_option]]}")
        
        # Move to next question or end quiz
        if st.session_state.current_question < len(data) - 1:
            st.session_state.current_question += 1
        else:
            st.write("Quiz completed! Your score is:", st.session_state.score)
            st.session_state.current_question = 0  # Reset for next run
            st.session_state.score = 0  # Reset score

if __name__ == "__main__":
    main()
