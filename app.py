import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# 1. Direct API Key
api_key = "AIzaSyAr-iEp9zgeo6Xn_qCjDe8j6aPTEiYLl6M"
genai.configure(api_key=api_key)

# 2. SMART AUTO-DETECT MODEL
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 2.5 wale models ko list se nikal do kyunke unki limit sirf 20 hai
    safe_models = [m for m in available_models if '2.5' not in m]
    
    if safe_models:
        working_model_name = safe_models[0] # Pehla safe model utha lo (jaise 2.0-flash ya 1.5-flash-8b)
    elif available_models:
        working_model_name = available_models[0] # Agar majboori hui toh jo mile utha lo
    else:
        st.error("⚠️ Aapki API key par koi text model available nahi hai.")
        st.stop()
        
    model = genai.GenerativeModel(working_model_name)
except Exception as e:
    st.error(f"⚠️ API Key check karne mein masla aaya: {e}")
    st.stop()

# 3. UI Setup
st.set_page_config(page_title="Faizan Automation System", layout="wide")
st.title("🎬 Faizan Automation System")
st.markdown("Yeh tool kisi bhi YouTube channel ke liye 3-second visual timeline generate karta hai.")

# 4. User Input
niche_input = st.selectbox("Video Niche / Style Select Karein:", 
                           ["Educational & Tech", "Business & Finance", "Horror & Mystery", "Funny & Entertainment", "Motivational", "General / Auto-Detect"])

script_input = st.text_area("Video Script Paste Karein:", height=200)

if st.button("Generate Timeline 🚀"):
    if not script_input.strip():
        st.warning("Pehle script enter karein!")
    else:
        with st.spinner(f"Timeline ban rahi hai ({working_model_name} use ho raha hai)..."):
            
            # 5. Offline Timing Logic
            words = script_input.split()
            chunk_size = 8
            chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            
            st.success(f"✅ Script ko {len(chunks)} hisson mein taqseem kar diya gaya hai. (Model Used: {working_model_name})")
            st.markdown("### 🎞️ Visual Timeline")
            
            # 6. Har hisse ke liye image banana
            for index, chunk in enumerate(chunks):
                col1, col2, col3 = st.columns([1, 3, 3])
                time_mark = index * 3
                
                with col1:
                    st.write(f"**⏱️ {time_mark}s - {time_mark+3}s**")
                with col2:
                    st.info(f"📜 **Spoken Text:**\n\n{chunk}")
                    
                with col3:
                    ai_prompt = f"Create a short, vivid, 1-sentence image generation prompt for this script snippet. The visual style and tone MUST perfectly match the '{niche_input}' niche. Script snippet: '{chunk}'. Return ONLY the prompt, nothing else."
                    
                    try:
                        # Step 1: Prompt generate karna 
                        response = model.generate_content(ai_prompt)
                        visual_prompt = response.text.strip()
                        st.write(f"🧠 **AI Prompt:** {visual_prompt}")
                        
                        # Step 2: Image ka URL banana
                        encoded_prompt = urllib.parse.quote(visual_prompt)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
                        
                        # Step 3: Browser ko direct load karne dena aur clickable link dena
                        st.image(image_url, use_container_width=True)
                        st.markdown(f"**[🔗 Click Here to View / Download Image]({image_url})**")
                        
                    except Exception as e:
                        st.error(f"Error aaya: {e}")
                
                st.divider()
                
                if index < len(chunks) - 1:
                    time.sleep(12) # API speed limit se bachne ke liye thora wait