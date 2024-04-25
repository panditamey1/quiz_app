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
    st.title("Quiz App")

    # Load CSV files from the "csvs" folder
    csvs_folder = "csvs"
    if not os.path.exists(csvs_folder):
        os.makedirs(csvs_folder)
        st.write("Please upload the CSV files to the 'csvs' folder")
    data = load_csvs(csvs_folder)

    # Randomize the order of the rows once and store in session state
    if 'data' not in st.session_state:
        st.session_state.data = data.sample(frac=1).reset_index(drop=True)
    
    # Initialize session state variables if not already present
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None

    # If the data is not empty, display the questions
    if not st.session_state.data.empty:
        question_data = st.session_state.data.loc[st.session_state.current_question]
        st.write(f"Question {st.session_state.current_question + 1}/{len(st.session_state.data)}")
        st.title(question_data['Learning Objective'])
        st.write(question_data['Question'])

        # Create shuffled options and store them
        if f'options_{st.session_state.current_question}' not in st.session_state:
            options_dict = {
                "A": question_data["Option A (Correct)"],
                "B": question_data["Option B (Incorrect)"],
                "C": question_data["Option C (Incorrect)"],
            }
            options = list(options_dict.values())
            random.shuffle(options)
            st.session_state[f'options_{st.session_state.current_question}'] = options

        # Use radio buttons for options
        selected_option = st.radio("Choose an answer:",
                                   st.session_state[f'options_{st.session_state.current_question}'],
                                   key=f'radio_{st.session_state.current_question}')

        # Submit button for the answer
        if st.button("Submit Answer"):
            st.session_state.selected_option = selected_option  # Store the selected option
            correct_answer = question_data["Option A (Correct)"]
            if selected_option == correct_answer:
                st.session_state.score += 1
                st.success(f"Correct! The answer is indeed: {correct_answer}")
            else:
                st.error(f"Wrong! The correct answer was: {correct_answer}")

            # Advance to the next question
            if st.session_state.current_question < len(st.session_state.data) - 1:
                st.session_state.current_question += 1
                st.experimental_rerun()  # Force rerun to refresh the state
            else:
                st.write(f"Quiz completed! Your final score is: {st.session_state.score}/{len(st.session_state.data)}")
                st.session_state.current_question = 0  # Reset for next run
                st.session_state.score = 0  # Reset score
                del st.session_state.data  # Optionally clear data to reload a new quiz

if __name__ == "__main__":
    main()
