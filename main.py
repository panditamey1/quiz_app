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
    st.title(data.loc[st.session_state.current_question, 'Learning Objective'])
    st.write(data.loc[st.session_state.current_question, 'Question'])
    options_dict = {
        data.loc[st.session_state.current_question, "Option A (Correct)"]: "Feedback A",
        data.loc[st.session_state.current_question, "Option B (Incorrect)"]: "Feedback B",
        data.loc[st.session_state.current_question, "Option C (Incorrect)"]: "Feedback C",
    }
    options = list(options_dict.keys())
    random.shuffle(options)

    # Option buttons and feedback display
    def handle_answer(index):
        option_chosen = options[index]
        if "Correct" in option_chosen:
            st.session_state.score += 1
            st.success("Correct! " + data.loc[st.session_state.current_question, options_dict[option_chosen]])
        else:
            st.error(f"Wrong! The correct answer was {data.loc[st.session_state.current_question, 'Option A (Correct)']}.\nFeedback: {data.loc[st.session_state.current_question, options_dict[option_chosen]]}")

    for i, option in enumerate(options):
        st.button(option.split('(')[0], on_click=handle_answer, args=(i,))

    # Next question button
    if st.button('Next Question'):
        if st.session_state.current_question < len(data) - 1:
            st.session_state.current_question += 1
        else:
            st.write("Quiz completed! Your score is:", st.session_state.score)
            st.session_state.current_question = 0  # Reset for next run
            st.session_state.score = 0  # Reset score

if __name__ == "__main__":
    main()
