import streamlit as st
import urllib.parse
import time

# 1. UI Setup
st.set_page_config(page_title="Faizan Automation System", layout="wide")
st.title("🎬 Faizan Automation System")
st.markdown("Yeh tool kisi bhi YouTube channel ke liye 3-second visual timeline generate karta hai.")

# 2. User Input
niche_input = st.selectbox("Video Niche / Style Select Karein:", 
                           ["Educational & Tech", "Business & Finance", "Horror & Mystery", "Funny & Entertainment", "Motivational", "General / Auto-Detect"])

script_input = st.text_area("Video Script Paste Karein:", height=200)

if st.button("Generate Timeline 🚀"):
    if not script_input.strip():
        st.warning("Pehle script enter karein!")
    else:
        with st.spinner("Timeline aur Free AI Images ban rahi hain (Super Fast Mode!)..."):
            
            # 3. Offline Timing Logic
            words = script_input.split()
            chunk_size = 8
            chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            
            st.success(f"✅ Script ko {len(chunks)} hisson mein taqseem kar diya gaya hai.")
            st.markdown("### 🎞️ Visual Timeline")
            
            # 4. Har hisse ke liye image banana (Bina kisi API text model ke!)
            for index, chunk in enumerate(chunks):
                col1, col2, col3 = st.columns([1, 3, 3])
                time_mark = index * 3
                
                with col1:
                    st.write(f"**⏱️ {time_mark}s - {time_mark+3}s**")
                with col2:
                    st.info(f"📜 **Spoken Text:**\n\n{chunk}")
                    
                with col3:
                    # Seedha aur simple prompt jo link ko tootne nahi dega
                    visual_prompt = f"{chunk}, {niche_input} style, highly detailed cinematic video scene"
                    st.write(f"🧠 **AI Prompt:** {visual_prompt}")
                    
                    try:
                        # Direct Image Generation
                        safe_prompt = urllib.parse.quote(visual_prompt)
                        # Random seed index takay har dafa nayi image aaye
                        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&seed={index + 50}"
                        
                        # Direct browser display (Sab se fast tareeqa)
                        st.image(image_url, use_container_width=True)
                                    
                    except Exception as e:
                        st.error(f"Error aaya: {e}")
                
                st.divider()
                time.sleep(1) # Chota sa break
