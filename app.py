import streamlit as st
from groq import Groq
import urllib.parse

# Page Configuration
st.set_page_config(page_title="Groq Powered AI Assistant", page_icon="⚡", layout="wide")

# API Keys Setup
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"  # <--- Apni Groq Key Yahan Dalein

if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
    st.warning("⚠️ Please apni Groq API Key code mein enter karein!")
else:
    # Groq Client Initialize karein
    client = Groq(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)

st.title("⚡ Ultra-Fast Groq AI Assistant")
st.write("Groq LPU ki speed, Image Generation, aur Professional Tone ke sath.")

# Chat history initialize karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Features
with st.sidebar:
    st.header("⚙️ Settings & Features")
    st.markdown("""
    - **Engine:** Groq LPU (Ultra Fast)
    - **Model:** `llama-3.3-70b-versatile` (Highly Professional)
    - **Image Generation:** Message ke shuru mein **"generate image:"** likhein.
    """)
    
    st.subheader("🎤 Voice Input")
    audio_value = st.audio_input("Record your voice")

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Generated Image")

# User Input
text_input = st.chat_input("Groq se kuch bhi poochahein...")
user_query = text_input if text_input else ""

# Processing the input
if user_query:
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "type": "text", "content": user_query})

    # 2. Check for IMAGE generation request
    if user_query.lower().startswith("generate image:"):
        prompt = user_query.split("generate image:")[1].strip()
        
        with st.chat_message("assistant"):
            with st.spinner("🖼️ Generating professional visual..."):
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42"
                
                st.image(image_url, caption=f"Result for: {prompt}")
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

    # 3. Handle TEXT with Groq (Professional Persona)
    else:
        with st.chat_message("assistant"):
            with st.spinner("⚡ Groq Processing..."):
                try:
                    # Professional System Prompt
                    system_prompt = (
                        "You are a highly professional, polite, and elite AI Corporate Assistant. "
                        "Always respond in a helpful, respectful, and sophisticated manner. "
                        "Avoid slang or informal language. If the user asks in Urdu/Hindi, "
                        "respond in polite, formal Roman Urdu or proper Urdu script. "
                        "Keep your safety filters high and refuse any inappropriate or harmful requests politely."
                    )

                    # Groq API Call
                    # Note: Llama-3.3-70b-versatile provides highly accurate and professional reasoning.
                    # content moderation and search intent are handled via advanced prompting here.
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            # Aap chahein toh yahan puri st.session_state.messages ki history bhi pass kar sakte hain
                            {"role": "user", "content": user_query}
                        ],
                        temperature=0.3, # Low temperature keeps it professional and factual
                        max_tokens=1024,
                    )
                    
                    bot_response = completion.choices[0].message.content
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": bot_response})
                    
                except Exception as e:
                    st.error(f"Groq System Error: {e}")
