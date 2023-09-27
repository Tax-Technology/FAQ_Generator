import streamlit as st
import openai
import base64

# Function to check if the provided API key is valid
def is_valid_api_key(api_key):
    try:
        # Attempt to set the OpenAI API key
        openai.api_key = api_key

        # Check if the key is valid by making a test request
        openai.Completion.create(engine="text-davinci-002", prompt="Test request", max_tokens=1)

        # If there are no exceptions, the key is valid
        return True
    except Exception as e:
        return False

# Define a function to generate FAQ using OpenAI API
def generate_faq(text, num_faqs, selected_tone, stop=None):
    # Define the prompt to instruct the model
    prompt = f"Generate {num_faqs} FAQs related to the following text: \"{text}\" with a {selected_tone} tone."

    try:
        # Use OpenAI's Completion API to generate FAQs
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50, # Adjust the max_tokens based on your needs
            n=num_faqs,    # Generate the specified number of FAQs
            stop=stop       # Allow the model to generate text freely
        )

        # Extract and return the generated FAQs
        qa_pairs = [{"question": qa.get('choices')[0].text.strip(), "answer": ""} for qa in response.choices]
        return qa_pairs
    except Exception as e:
        st.error("An error occurred while generating FAQs.")
        st.exception(e)
        return []

# Define a function to display the FAQ
def display_faq(qa_pairs):
    for qa in qa_pairs:
        st.markdown(f"**Q:** {st.markdown(qa['question'])}")
        st.markdown(f"**A:** {st.markdown(qa['answer'])}")
        st.markdown("---")

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
    # Check if the user has entered a valid OpenAI API key
    if api_key and is_valid_api_key(api_key):
        # Generate questions and answers using OpenAI API based on user-selected options
        qa_pairs = generate_faq(text_input, num_faqs, selected_tone)

        # Display the FAQ
        display_faq(qa_pairs)
    else:
        st.error("Please enter a valid OpenAI API key.")
