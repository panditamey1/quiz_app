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
def gen_quiz(question_number,df, key="my-form"):
    form = st.form(key=key)
    question = question_number
    form.write(f"Question {question_number + 1}")
    form.write(df.loc[question, "Question"])
    # Learning Objective,Question,Option A (Correct),Option B (Incorrect),Option C (Incorrect),Feedback A,Feedback B,Feedback C
    # create dictionary of options and then shuffle
    options_dict = {
        df.loc[question, "Option A (Correct)"]: df.loc[question, "Feedback A"],
        df.loc[question, "Option B (Incorrect)"]: df.loc[question, "Feedback B"],
        df.loc[question, "Option C (Incorrect)"]: df.loc[question, "Feedback C"],
    }
    list_of_options = list(options_dict.items())
    random.shuffle(list_of_options)
    
    correct_answer = df.loc[question, "Option A (Correct)"]
    incorrect_answers = df.loc[question, ["Option B (Incorrect)", "Option C (Incorrect)"]].dropna()

    options = [correct_answer] + list(incorrect_answers)
    random.shuffle(options)

    selected_answer = form.radio("Options", options)
    submit = form.form_submit_button("Submit")
    if submit:
        if selected_answer == correct_answer:
            form.write("Correct!")
            form.info("Explanation: " + options_dict[correct_answer])
        else:
            form.write(f"Wrong! The correct answer is {correct_answer}")
            form.info("Explanation: " + df.loc[question, 'Feedback A'])
            form.info ("Feedback for other options:")
            for option in incorrect_answers:
                form.info(f"{option}: {options_dict[option]}")




def main():
    # Load CSV files from the "csvs" folder
    csvs_folder = "csvs"
    if not os.path.exists(csvs_folder):
        os.makedirs(csvs_folder)
        # give option to upload files
        st.write("Please upload the CSV files to the 'csvs' folder")

    st.title("Quiz App")

    df = load_csvs(csvs_folder)

    # Randomize the order of the rows
    df = df.sample(frac=1).reset_index(drop=True)

    # form2 = st.form(key="my-form-2")
    st.session_state.question_number = 0
    # next_question = form2.number_input(
    #     "Question Number:", min_value=0, max_value=len(df)-1, value=st.session_state.question_number, key="question_number"
    # )
    
    
    # next_question_button = form2.form_submit_button("Next Question")
    # if next_question_button:
    #     next_question += 1
    #     st.session_state.question_number = next_question
    
    question = st.session_state.question_number
    if st.session_state.question_number == 0:
        gen_quiz(st.session_state.question_number,df)
    next_question_button = st.button("Next Question")
    if next_question_button:
        question += 1
        st.session_state.question_number = question
        gen_quiz(question,df)

    # Display the questions one by one
    
if __name__ == "__main__":
    main()