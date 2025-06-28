import streamlit as st
from openai import OpenAI
from groq import Groq
from google import genai
from google.genai import types
from core.config import config

#Lets create a sidebar with a dropdown for the model list and providers 
with st.sidebar:
    st.title("Settings")
    provider = st.selectbox("Select a provider", ["openai", "groq", "google"])
    if provider == "openai":
        model_name = st.selectbox("Select a model", ["gpt-4o-mini", "gpt-4o"])
    elif provider == "groq":
        model_name = st.selectbox("Select a model", ["llama-3.3-70b-versatile"])
    elif provider == "google":
        model_name = st.selectbox("Select a model", ["gemini-2.0-flash"])

    #Save provider and model to session state
    st.session_state.provider = provider
    st.session_state.model_name = model_name
    
    # Add a slider for the temperature
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    st.session_state.temperature = temperature

    # Add a slider between 0 and 500 that controls the max_tokens
    max_tokens = st.slider("Max Tokens", min_value=0, max_value=500, value=500, step=10)
    st.session_state.max_tokens = max_tokens


if provider == "openai":
    client = OpenAI(api_key=config.openai_api_key)
elif provider == "groq":
    client = Groq(api_key=config.groq_api_key)
elif provider == "google":
    client = genai.Client(api_key=config.google_api_key)

# Run LLM function for processing Google Models
def run_llm(client, messages):
    if st.session_state.provider == "google":
        return client.models.generate_content(
            model=st.session_state.model_name,
            contents=[message["content"] for message in messages],
            config=types.GenerateContentConfig(
                max_output_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature
            )
            
        ).text
    else:
        return client.chat.completions.create(
            model=st.session_state.model_name,
            messages=messages,
            max_tokens=st.session_state.max_tokens,
            temperature=st.session_state.temperature
        ).choices[0].message.content    

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# Initialize session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello! How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = run_llm(client, st.session_state.messages)
        st.write(output)
    st.session_state.messages.append({"role": "assistant", "content": str(output) if output is not None else "No response generated"})