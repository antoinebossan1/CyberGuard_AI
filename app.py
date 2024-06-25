import streamlit as st
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from model_interaction import interact_with_model
from mistralai.client import MistralClient
from dotenv import load_dotenv
load_dotenv()

st.title("CyberGuard AI: Advanced AI-Driven Cybersecurity Advisor 🛡️")
st.caption("Leveraging Mistral's Fine-Tuning API with LoRA for Real-Time DDos Threat Detection and Response")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please input the network log data to classify the threat."}]
  
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=10, memory_key="chat_history", return_messages=True)

def format_history(messages):
    formatted = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted += f"{role}: {msg['content']}\n"
    return formatted

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    conversation_history = format_history(st.session_state.messages)

    prompt_template = PromptTemplate(
        input_variables=["history", "context", "question"],
        template="Conversation History:\n{history}\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:",
    )

    formatted_prompt = prompt_template.format(history=conversation_history, context="", question=prompt)

    print(f'Formatted Prompt: {formatted_prompt}')
    
    fine_tuned_model = 'ft:open-mistral-7b:a8d1498d:20240625:f4347a45' 
    print(f"Interacting with model {fine_tuned_model} with API key: {os.environ.get('MISTRAL_API_KEY')}")

    client = MistralClient(api_key=os.environ.get("MISTRAL_API_KEY"))

    response = interact_with_model(client,fine_tuned_model, formatted_prompt)

    response_content = response.choices[0].message.content if response.choices else "No response from model."
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    st.chat_message("assistant").write(response_content)
