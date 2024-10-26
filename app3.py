import streamlit as st
from groq import Groq
from langdetect import detect, DetectorFactory
from mtranslate import translate
from googlesearch import search

# Set consistent seed for langdetect
DetectorFactory.seed = 0

# API key for Groq
API_KEY = "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"

# Initialize the Groq client with the API key
try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    client = None  

# Function to get references from search results
def get_references(query):
    results = []
    try:
        # Perform a Google search and collect the URLs
        for url in search(query):
            if not any(excluded in url for excluded in ["reddit.com", "quora.com"]):
                results.append(url)
                if len(results) >= 5:  # Limit to 5 results
                    break
    except Exception as e:
        st.error(f"Error fetching references: {e}")
    return results

# Streamlit app title
st.title("Drona Chatbot")

# Initialize session state to store conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display the conversation history
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Assistant:** {message['content']}")

# Create a container for the input area
input_container = st.container()

with input_container:
    # Create a row with two columns
    col1, col2 = st.columns([3, 1])  # Adjust the proportions as needed

    # User input
    user_input = col1.text_input("Ask a question:", placeholder="Type your question here...", key="user_input")  # Unique key for the text input
    submit_button = col2.button("Submit")

    if submit_button:
        if user_input:
            if client is not None:
                try:
                    # Detect the language of the user input
                    detected_language = detect(user_input)
                    
                    # Translate to English if input is in another language
                    if detected_language != "en":
                        translated_input = translate(user_input, 'en', detected_language)
                        st.write(f"Translated Input: {translated_input}")
                    else:
                        translated_input = user_input

                    # Append the translated (or original English) user message to conversation history
                    st.session_state.conversation_history.append({"role": "user", "content": translated_input})
                    
                    # Prepare the chat completion request
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=st.session_state.conversation_history,
                        temperature=1,
                        max_tokens=1500,
                        top_p=1,
                        stream=True,
                        stop=None,
                    )

                    # Collect the response chunks
                    response_text = ""
                    for chunk in completion:
                        response_content = chunk.choices[0].delta.content
                        if response_content:
                            response_text += response_content  # Concatenate the response

                    # Translate response back to the user's language if necessary
                    if detected_language != "en":
                        translated_response = translate(response_text, detected_language, 'en')
                    else:
                        translated_response = response_text

                    # Get references for the response
                    references = get_references(user_input)
                    reference_links = "\n".join(references)

                    # Display the response with reference links
                    st.write("Response:")
                    st.write(translated_response)
                    st.write("References:")
                    st.write(reference_links)

                    # Append assistant's response to conversation history
                    st.session_state.conversation_history.append({"role": "assistant", "content": translated_response})
                    
                except Exception as e:
                    st.error(f"Error during completion: {e}")
            else:
                st.error("The Groq client could not be initialized. Please check your configuration.")
        else:
            st.warning("Please enter a question.")

# Show the detected language information (can be moved inside the main logic if needed)
if "detected_language" in st.session_state:
    st.subheader("Detected Language:")
    st.write(st.session_state["detected_language"])
