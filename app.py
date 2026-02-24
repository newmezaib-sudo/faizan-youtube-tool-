import streamlit as st
import requests
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
        with st.spinner("Timeline aur High-Quality AI Images aa rahi hain..."):
            
            # 3. Offline Timing Logic
            words = script_input.split()
            chunk_size = 8
            chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            
            st.success(f"✅ Script ko {len(chunks)} hisson mein taqseem kar diya gaya hai.")
            st.markdown("### 🎞️ Visual Timeline")
            
            # 4. Har hisse ke liye AI Image dhoondna (Lexica AI se)
            for index, chunk in enumerate(chunks):
                col1, col2, col3 = st.columns([1, 3, 3])
                time_mark = index * 3
                
                with col1:
                    st.write(f"**⏱️ {time_mark}s - {time_mark+3}s**")
                with col2:
                    st.info(f"📜 **Spoken Text:**\n\n{chunk}")
                    
                with col3:
                    # Lexica ke liye smart search query
                    search_query = f"{chunk} {niche_input} cinematic"
                    st.write(f"🧠 **AI Search Query:** {search_query}")
                    
                    try:
                        # Lexica API - Instant & Free AI Images (No API Key!)
                        url = f"https://lexica.art/api/v1/search?q={urllib.parse.quote(search_query)}"
                        response = requests.get(url, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if "images" in data and len(data["images"]) > 0:
                                # Sab se pehli aur best AI tasweer uthana
                                image_url = data["images"][0]["src"]
                                st.image(image_url, use_container_width=True)
                            else:
                                st.warning("⚠️ Is line se match karti AI image nahi mili.")
                        else:
                            st.error("⚠️ Server busy hai.")
                                    
                    except Exception as e:
                        st.error(f"Error aaya: {e}")
                
                st.divider()
                time.sleep(1) # Chota sa break
