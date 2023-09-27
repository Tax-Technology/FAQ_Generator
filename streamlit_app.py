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

# Function to generate FAQ questions using OpenAI API
def generate_questions(text, num_questions, selected_tone):
    try:
        prompt = f"Generate {num_questions} questions related to the following text: \"{text}\" with a {selected_tone} tone."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,  # Adjust max_tokens as needed for longer answers
            n=num_questions,
            stop=None
        )
        return response.choices
    except Exception as e:
        st.error("An error occurred while generating questions.")
        st.exception(e)
        return []

# Function to answer questions using OpenAI API
def answer_questions(text, questions):
    try:
        qa_pairs = []
        for question in questions:
            prompt = f"Answer the following question using the provided text: \"{question['text']}\""
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200,  # Adjust max_tokens as needed for longer answers
                n=1,
                stop=None
            )
            qa_pairs.append((question['text'], response.choices[0]['text'].strip()))
        return qa_pairs
    except Exception as e:
        st.error("An error occurred while answering questions.")
        st.exception(e)
        return []

# Create a Streamlit app
st.title("Question and Answer Generator")

# Add a text input widget for entering the OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Add a slider to select the number of questions to generate (between 1 and 10)
num_questions = st.slider("Number of Questions to Generate", 1, 10, 5)

# Add a selectbox to choose the tone
selected_tone = st.selectbox("Select Tone", ["friendly", "professional", "technical"])

# Add a text area for entering text, with a 5000-word limit
text_input = st.text_area("Enter your text here (maximum 5000 words)")

# Define a submit button
if st.button("Generate Questions and Answers", key="generate_button"):
    if api_key and is_valid_api_key(api_key) and text_input:
        with st.spinner("Generating Questions and Answers..."):
            questions = generate_questions(text_input, num_questions, selected_tone)
            qa_pairs = answer_questions(text_input, questions)

        # Create a DataFrame for questions and answers
        data = {"Question": [], "Answer": []}
        for qa_pair in qa_pairs:
            question = qa_pair[0]
            answer = qa_pair[1]
            data["Question"].append(question)
            data["Answer"].append(answer)

        df = pd.DataFrame(data)

        # Display questions and answers in a markdown table
        st.markdown("### Questions and Answers")
        st.write(df)
    else:
        st.error("Please enter a valid OpenAI API key and some text before generating questions and answers.")
