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
        # give option to upload files
        st.write("Please upload the CSV files to the 'csvs' folder")
        
    st.title("Quiz App")

    df = load_csvs(csvs_folder)

    # Randomize the order of the rows
    df = df.sample(frac=1).reset_index(drop=True)

    # Display the questions one by one
    for index, row in df.iterrows():
        st.write(f"**{row['Learning Objective']}**")
        st.write(f"{row['Question']}")

        # Randomize the order of the options
        options = [row['Option A (Correct)'], row['Option B (Incorrect)'], row['Option C (Incorrect)']]
        random.shuffle(options)

        # Get user's answer
        user_answer = st.radio("Select your answer", options)

        # Check if the user's answer is correct
        if user_answer == row['Option A (Correct)']:
            st.success(f"Correct! {row['Feedback A']}")
        elif user_answer == row['Option B (Incorrect)']:
            st.error(f"Incorrect. {row['Feedback B']}")
        else:
            st.error(f"Incorrect. {row['Feedback C']}")

        # Move to the next question
        if st.button("Next Question"):
            continue

if __name__ == "__main__":
    main()