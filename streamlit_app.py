import streamlit as st
import openai

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
            max_tokens=50,
            n=num_faqs,
            stop=None
        )
        return [{"question": qa["text"].strip(), "answer": ""} for qa in response.choices]
    except Exception as e:
        st.error("An error occurred while generating FAQs.")
        st.exception(e)
        return []

# Function to display the FAQ
def display_faq(qa_pairs):
    for qa in qa_pairs:
        st.markdown(f"**Q:** {qa['question']}")
        st.markdown(f"**A:** {qa['answer']}")
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
    if api_key and is_valid_api_key(api_key) and text_input:
        with st.spinner("Generating FAQs..."):
            qa_pairs = generate_faq(text_input, num_faqs, selected_tone)
        display_faq(qa_pairs)
    else:
        st.error("Please enter a valid OpenAI API key and some text before generating FAQs.")
