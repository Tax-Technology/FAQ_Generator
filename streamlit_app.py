import streamlit as st
import openai

# Function to check if the provided API key is valid
def is_valid_api_key(api_key):
  """Checks if the provided API key is valid.

  Args:
    api_key: The API key to check.

  Returns:
    True if the API key is valid, False otherwise.
  """

  try:
    openai.api_key = api_key
    openai.Completion.create(engine="text-davinci-002", prompt="Test request", max_tokens=1)
    return True
  except Exception as e:
    return False

# Function to generate a question using OpenAI
def generate_question(text, selected_tone):
  """Generates a question using the OpenAI API.

  Args:
    text: The text to generate the question for.
    selected_tone: The tone of the question.

  Returns:
    A string containing the generated question.
  """

  prompt = f"Generate a question related to the following text: \"{text}\" with a {selected_tone} tone."
  response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=100,
      n=1,
      stop=None
  )
  return response.choices[0].text.strip()

# Function to generate an answer to a question using OpenAI
def generate_answer(question, text, selected_tone):
  """Generates an answer to a question using the OpenAI API.

  Args:
    question: The question to generate the answer for.
    text: The text to generate the answer from.
    selected_tone: The tone of the answer.

  Returns:
    A string containing the generated answer.
  """

  prompt = f"Generate an answer to the following question: \"{question}\" based on the following text: \"{text}\" with a {selected_tone} tone."
  response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=200,
      n=1,
      stop=None
  )
  return response.choices[0].text.strip()

# Create a Streamlit app
st.title("Question and Answer Generator")

# Add a text input widget for entering the OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Add a selectbox to choose the tone
selected_tone = st.selectbox("Select Tone", ["friendly", "professional", "technical"])

# Add a text area for entering text, with a 5000-word limit
text_input = st.text_area("Enter your text here (maximum 5000 words)")

# Define a submit button
if st.button("Generate Question and Answer", key="generate_button"):
  if api_key and is_valid_api_key(api_key) and text_input:
    with st.spinner("Generating Question and Answer..."):
      # Generate a question
      question = generate_question(text_input, selected_tone)

      # Generate an answer to the question, using the user's text as context
      answer = generate_answer(question, text_input, selected_tone)

      # Display the question and answer to the user
      st.write("Generated Question:")
      st.write(question)
      st.write("Generated Answer:")
      st.write(answer)

  else:
    st.error("Please enter a valid OpenAI API key and some text before generating the question and answer pairs.")
