from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

st.set_page_config(page_title="ASK YOUR Sheet")

def main():
    api_key = st.text_input("Enter your OpenAI API Key")
    
    st.header("Ask your Sheet")

    Sheet = st.file_uploader("Upload your Excel Sheet", type="xlsx")

    if Sheet is not None:  # Check if a file is uploaded
        try:
            df = pd.read_excel(Sheet)
        except Exception as e:
            st.write(f"Error reading the Excel file: {e}")
            return

        # Convert the data into a single string
        text = ' '.join(df.stack().astype(str))

        if api_key:
            client = OpenAI(api_key=api_key)
        else:
            st.write("Please enter your OpenAI API Key.")

        # Define your messages
        messages = [
            # {"role": "system", "content": "You are a helpful assistant and very very knowledgeable about CEFR levels. and only give a two word answer for each word, which is the word it self and it's CEFR level for all the words entered and do this very very carefully so that there are no Mistakes do the same and give the answer in the form abondon C1 Ability B1 etc"},
            {"role": "system", "content": "You are a helpful assistant and very very knowledgeable about CEFR levels. and only give a one word answer for each word, which is the CEFR level for each of the words entered and do this very very carefully so that there are no Mistakes do the same and give the answer in the form A1 C1 B1 A2 etc"},
            {"role": "user", "content": text}
        ]

        # Call the OpenAI API to get the completion
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=100
            )
        except Exception as e:
            st.write(f"Error communicating with OpenAI API: {e}")
            return

        # Get the answer from the API response
        answer = response.choices[0].message.content

        # Break line after every two words
        words = answer.split()
        # answer_with_newlines = '<br>'.join(' '.join(words[i:i+2]) for i in range(0, len(words), 2))
        answer_with_newlines = '<br>'.join(words)

        # Display the answer with line breaks in Streamlit using st.markdown()
        st.markdown(answer_with_newlines, unsafe_allow_html=True)
    else:
        st.write("Please upload a valid Excel file.")

if __name__ == '__main__':
    main()
