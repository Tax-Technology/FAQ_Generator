import streamlit as st
from transformers import pipeline

# Load the generative AI model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased", framework=None)

# Define the main function
def main():
  # Create a Streamlit app
  st.title("FAQ Generator")

  # Add a text input widget
  text_input = st.text_area("Enter your text here")

  # Check if the user has entered text
  if text_input:
    # Parse the text and formulate questions and answers
    qa_pairs = parse_text_to_faq(text_input)

    # Display the FAQ
    display_faq(qa_pairs)

# Define a function to parse the text and formulate questions and answers
def parse_text_to_faq(text):
    """Parses the given text and formulates questions and answers using generative AI.

    Args:
        text: A string containing the text to be parsed.

    Returns:
        A list of dictionaries, where each dictionary contains a question and its
        corresponding answer.
    """

    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    # Generate questions and answers for each paragraph
    qa_pairs = []
    for paragraph in paragraphs:
        # Ensure that the input is in the correct format (SquadExample or dictionary)
        input_data = {
            "question": "What is in this paragraph?",  # You can customize the question here
            "context": paragraph,
        }

        # Use the qa_pipeline with the formatted input
        questions = qa_pipeline(input_data)

        if questions:
            # Append the generated answer to the qa_pairs
            qa_pairs.append({"question": input_data["question"], "answer": questions[0]["answer"]})

    return qa_pairs

# Define a function to display the FAQ
def display_faq(qa_pairs):
    """Displays the given FAQ in a Streamlit app.

    Args:
        qa_pairs: A list of dictionaries, where each dictionary contains a question and its
        corresponding answer.
    """

    # If the FAQ list is empty, display a message
    if not qa_pairs:
        st.write("No questions and answers found.")
    else:
        # Create a table to display the FAQ
        table = st.table(headers=["Question", "Answer"])
        for qa_pair in qa_pairs:
            table.add_row(qa_pair["question"], qa_pair["answer"])

if __name__ == "__main__":
    main()
