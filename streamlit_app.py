import streamlit as st
import openai
import base64

# Create a Streamlit app
st.title("FAQ Generator")

# Add a text input widget for entering the OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Add a slider to select the number of FAQs to generate (between 1 and 10)
num_faqs = st.slider("Number of FAQs to Generate", 1, 10, 5)

# Add a selectbox to choose the tone
selected_tone = st.selectbox("Select Tone", ["friendly", "professional", "technical"])

# Define the main function
def main():
    # Add a text input widget
    text_input = st.text_area("Enter your text here")

    # Check if the API key is provided and valid
    if api_key and is_valid_api_key(api_key):
        if st.button("Generate FAQs"):
            # Generate questions and answers using OpenAI API based on user-selected options
            qa_pairs = generate_faq(text_input, num_faqs, selected_tone)

            # Display the FAQ
            display_faq(qa_pairs)

        # Add a button to clear the input and FAQs
        if st.button("Clear Input and FAQs"):
            clear_input_and_faqs()
        
        # Add a button to save FAQs to a file
        if st.button("Save FAQs to File"):
            save_faqs_to_file(qa_pairs)
    else:
        st.warning("Please enter a valid OpenAI API key.")

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
def generate_faq(text, num_faqs, selected_tone):
    # Rest of the code remains the same as in the previous example

# Define a function to display the FAQ
def display_faq(qa_pairs):
    # Corrected indentation below
    for qa in qa_pairs:
        st.markdown(f"**Q:** {qa['question']}")
        st.write(f"**A:** {qa['answer']}")
        st.write("---")

# Function to clear input and FAQs
def clear_input_and_faqs():
    st.text_input.label(widget="Clearing input and FAQs...")
    st.text_area(label="", value="", key="text_input")
    st.empty()

# Function to save FAQs to a file
def save_faqs_to_file(qa_pairs):
    if not qa_pairs:
        st.warning("No FAQs to save.")
        return
    
    # Create a download link for saving FAQs to a text file
    faq_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\n" for qa in qa_pairs])
    st.markdown(get_binary_file_downloader_html(faq_text, file_name="generated_faqs.txt"), unsafe_allow_html=True)

# Function to create a download link for saving FAQs to a file
def get_binary_file_downloader_html(bin_data, file_name, button_text="Download FAQs"):
    bin_str = bin_data.encode().decode('utf-8').encode('latin-1')
    b64 = base64.b64encode(bin_str).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{file_name}">{button_text}</a>'

if __name__ == "__main__":
    main()
