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
    options = df.loc[question, "Options"].split(", ")
    correct_answer = df.loc[question, "Answer"]
    user_answer = form.radio("Options", options)
    if user_answer == correct_answer:
        form.write("Correct!")
    else:
        form.write(f"Wrong! The correct answer is {correct_answer}")
    form.write("Explanation")
    form.write(df.loc[question, "Explanation"])



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
    curr_question = st.number_input(
            "Question Number:", min_value=0, max_value=len(df)-1, value=0, step=1
        )

    gen_quiz(curr_question,df)


    # Display the questions one by one
    
if __name__ == "__main__":
    main()