import streamlit as st
import openai
import pandas as pd

# Function to check if the provided API key is valid
def is_valid_api_key(api_key):
    try:
        openai.api_key = api_key
        openai.Completion.create(engine="text-davinci-002", prompt="Test request", max_tokens=1)
        return True
    except Exception as e:
        return False

# Function to generate FAQ using OpenAI API
def generate_faq(text, num_faqs, selected_tone):
    try:
        prompt = f"Generate {num_faqs} FAQs related to the following text: \"{text}\" with a {selected_tone} tone."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,  # Adjust max_tokens as needed for longer answers
            n=num_faqs,
            stop=None
        )
        return response.choices
    except Exception as e:
        st.error("An error occurred while generating FAQs.")
        st.exception(e)
        return []

# Create a Streamlit app
st.title("FAQ Generator")

# Add a text input widget for entering the OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Add a slider to select the number of FAQs to generate (between 1 and 10)
num_faqs = st.slider("Number of FAQs to Generate", 1, 10, 5)

# Add a selectbox to choose the tone
selected_tone = st.selectbox("Select Tone", ["friendly", "professional", "technical"])

# Add a text area for entering text, with a 5000-word limit
text_input = st.text_area("Enter your text here (maximum 5000 words)")

# Define a submit button
if st.button("Generate FAQs", key="generate_button"):
    if api_key and is_valid_api_key(api_key) and text_input:
        with st.spinner("Generating FAQs..."):
            qa_pairs = generate_faq(text_input, num_faqs, selected_tone)

        # Create a DataFrame for questions and answers
        data = {"Question": [], "Answer": []}
        for i, qa in enumerate(qa_pairs):
            question = qa['text'].strip()
            data["Question"].append(f"Q{i + 1}: {question}\n")
            data["Answer"].append(f"A{i + 1}: {question}\n")  # Use the same question as answer for now

        df = pd.DataFrame(data)

        # Display questions and answers in a markdown table
        st.markdown("### Generated FAQs")
        st.write(df)  # Use st.write instead of st.markdown for DataFrames
    else:
        st.error("Please enter a valid OpenAI API key and some text before generating FAQs.")
