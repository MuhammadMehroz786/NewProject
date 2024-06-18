import streamlit as st
import pandas as pd
from openai import OpenAI

def main():
    st.set_page_config(page_title="ASK YOUR Sheet")
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

        # Set your OpenAI API key
        client = OpenAI(api_key="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")

        # Define your messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant and very very knowledgeable about CEFR levels. and only give a two word answer for each word, which is the word it self and it's CEFR level for all the words entered and do this very very carefully so that there are no Mistakes  do the same and give the answer in the form abondon C1 Ability B1 etc"},
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
        answer_with_newlines = '<br>'.join(' '.join(words[i:i+2]) for i in range(0, len(words), 2))

        # Display the answer with line breaks in Streamlit using st.markdown()
        st.markdown(answer_with_newlines, unsafe_allow_html=True)
    else:
        st.write("Please upload a valid Excel file.")

if __name__ == '__main__':
    main()
