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

  # Add a submit button
  if st.button("Generate FAQs"):
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
    questions = qa_pipeline(paragraph)
    for question in questions:
      if "question" in question and "answer" in question:
        answer = qa_pipeline(question["answer"], paragraph)["answer"]
        qa_pairs.append({"question": question["question"], "answer": answer})

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
