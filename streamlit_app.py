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
    # Generate questions and answers based on the provided text
    qa_pairs = generate_faq_from_text(text_input)

    # Display the FAQ
    display_faq(qa_pairs)

# Define a function to generate questions and answers from the provided text
def generate_faq_from_text(text):
  """Generates questions and answers based on the provided text.

  Args:
    text: A string containing the text to generate questions and answers from.

  Returns:
    A list of dictionaries, where each dictionary contains a generated question and its
    corresponding answer.
  """
  
  # Define the question you want to ask about the text
  question = "What information can you provide about this text?"
  
  # Use the qa_pipeline with the provided text and question
  questions = qa_pipeline(context=text, question=question)

  # Extract the generated answer
  answer = questions[0]["answer"]

  # Return the generated question and answer pair
  return [{"question": question, "answer": answer}]

# Define a function to display the FAQ
def display_faq(qa_pairs):
  """Displays the generated FAQ in a Streamlit app.

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
