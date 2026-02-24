import streamlit as st
from bytez import Bytez
import urllib.parse
import time

# 1. Text Engine Setup (Bytez - Jo bilkul theek chal raha hai)
bytez_api_key = "d5085219e259c1cd826160c24906dc05"
bytez_client = Bytez(bytez_api_key)
text_model = bytez_client.model("Qwen/Qwen2-7B-Instruct")

# 2. UI Setup
st.set_page_config(page_title="Faizan Automation System", layout="wide")
st.title("🎬 Faizan Automation System")
st.markdown("Yeh tool kisi bhi YouTube channel ke liye 3-second visual timeline generate karta hai.")

# 3. User Input
niche_input = st.selectbox("Video Niche / Style Select Karein:", 
                           ["Educational & Tech", "Business & Finance", "Horror & Mystery", "Funny & Entertainment", "Motivational", "General / Auto-Detect"])

script_input = st.text_area("Video Script Paste Karein:", height=200)

if st.button("Generate Timeline 🚀"):
    if not script_input.strip():
        st.warning("Pehle script enter karein!")
    else:
        with st.spinner("Timeline aur Free AI Images ban rahi hain (Bina kisi API Key ke!)..."):
            
            # 4. Offline Timing Logic
            words = script_input.split()
            chunk_size = 8
            chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            
            st.success(f"✅ Script ko {len(chunks)} hisson mein taqseem kar diya gaya hai.")
            st.markdown("### 🎞️ Visual Timeline")
            
            # 5. Har hisse ke liye image banana
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
                        # Step 1: Text Engine se AI Prompt nikalna
                        result = text_model.run(ai_prompt)
                        is_dict = isinstance(result, dict)
                        txt_output = result.get("output") if is_dict else getattr(result, "output", None)
                        visual_prompt = str(txt_output).strip() if txt_output else f"High quality cinematic visual matching: {chunk}"
                        st.write(f"🧠 **AI Prompt:** {visual_prompt}")
                        
                        # Step 2: Pollinations AI (NO API KEY REQUIRED!)
                        with st.spinner("🖼️ Generating AI Image..."):
                            # Text ko URL ke qabil banana
                            safe_prompt = urllib.parse.quote(visual_prompt)
                            # Direct Image URL (1280x720 HD)
                            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&seed={index}"
                            
                            st.image(image_url, use_container_width=True)
                                    
                    except Exception as e:
                        st.error(f"Error aaya: {e}")
                
                st.divider()
                time.sleep(1) # Chota sa break
