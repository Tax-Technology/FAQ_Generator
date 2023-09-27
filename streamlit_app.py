import streamlit as st
import openai

# Function to check if the provided API key is valid
def is_valid_api_key(api_key):
    # (Same as before)

# Function to generate a question using OpenAI
def generate_question(text, selected_tone):
    # (Same as before)

# Function to generate an answer to a question using OpenAI
def generate_answer(question, text, selected_tone):
    # (Same as before)

# Create a Streamlit app
st.title("Question and Answer Generator")

# Add a text input widget for entering the OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Add a selectbox to choose the tone
selected_tone = st.selectbox("Select Tone", ["friendly", "professional", "technical"])

# Add a text area for entering text, with a 5000-word limit
text_input = st.text_area("Enter your text here (maximum 5000 words)")

# Add a number input for specifying the number of pairs to generate
num_pairs = st.number_input("Number of Question & Answer pairs to generate", min_value=1, max_value=10, value=1)

# Define a submit button
if st.button("Generate Question and Answer", key="generate_button"):
    if api_key and is_valid_api_key(api_key) and text_input and num_pairs >= 1:
        with st.spinner("Generating Question and Answer pairs..."):
            # Initialize a list to store the generated pairs
            pairs = []

            for _ in range(num_pairs):
                # Generate a question
                question = generate_question(text_input, selected_tone)

                # Generate an answer to the question, using the user's text as context
                answer = generate_answer(question, text_input, selected_tone)

                # Add the pair to the list
                pairs.append((question, answer))

            # Display the generated question and answer pairs to the user
            for i, (question, answer) in enumerate(pairs, start=1):
                st.write(f"Pair {i}:")
                st.write("Generated Question:")
                st.write(question)
                st.write("Generated Answer:")
                st.write(answer)

    else:
        st.error("Please enter a valid OpenAI API key, some text, and a valid number of pairs (1-10) before generating.")
