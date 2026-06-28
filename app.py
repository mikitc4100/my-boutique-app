import streamlit as st
import requests
import base64

# Page Setup for Premium Brand Look
st.set_page_config(page_title="Laxmi Boutique", page_icon="👗", layout="centered")

# --- 👑 COLOURED BRAND LOGO INTEGRATION ---
# Yeh AI wala logo direct online load hokar aapki app me sabse upar dikhega
logo_url = "https://githubusercontent.com"
st.image(logo_url, use_container_width=True)

st.title("👑 Laxmi Boutique Premium Hub 👑")
st.subheader("✨ Where Elegance Meets Tradition ✨")
st.write("Apne customers ko latest premium designs dikhayein aur mobile se live photos manage karein!")

# 🔑 --- IMGBB FREE API STORAGE CONFIG ---
# Yahan par apni vahi purani ImgBB API Key brackets ke andar paste rehne dena
IMGBB_API_KEY = "YOUR_API_KEY_HERE"

# --- 📂 CUSTOM BOUTIQUE FOLDERS ---
categories = [
    "👗 Kurti Designs",
    "📐 Neck Designs",
    "👚 Blouse Designs",
    "👰 Lehenga Designs",
    "👖 Pant Plazo Designs",
    "👔 Collar Designs",
    "🦾 Sleeve Designs",
    "📁 Custom Category 1",
    "📁 Custom Category 2"
]

# Permanent Session Storage Setup
if "gallery" not in st.session_state:
    st.session_state.gallery = {cat: [] for cat in categories}

# Sidebar Navigation Control
st.sidebar.markdown("### 🏢 Laxmi Boutique Admin")
app_mode = st.sidebar.radio("Go to Options:", ["👀 View Design Gallery", "📤 Upload New Designs"])

# ==========================================
# MODE 1: UPLOAD DESIGNS
# ==========================================
if app_mode == "📤 Upload New Designs":
    st.header("📤 Upload Latest Masterpieces")
    selected_cat = st.selectbox("Kaun se folder me photo daalni hai?", categories)
    uploaded_file = st.file_uploader("Mobile Camera ya Gallery se Photo chuno:", type=["jpg", "png", "jpeg"])
    
    if st.button("Upload to Cloud 🚀") and uploaded_file is not None:
        with st.spinner("Design Cloud me save ho raha hai..."):
            try:
                img_bytes = uploaded_file.read()
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                payload = {
                    "key": IMGBB_API_KEY,
                    "image": base64_image
                }
                response = requests.post("https://imgbb.com", data=payload)
                res_data = response.json()
                
                if response.status_code == 200:
                    image_url = res_data["data"]["url"]
                    st.session_state.gallery[selected_cat].append(image_url)
                    st.success(f"✅ Design successfully **{selected_cat}** folder me save ho gaya!")
                else:
                    st.error(f"Upload fail: {res_data['error']['message']}")
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# MODE 2: VIEW GALLERY
# ==========================================
else:
    st.header("🖼️ Explore Luxury Collections")
    view_cat = st.selectbox("Select Category to View:", categories)
    
    st.markdown("---")
    images_list = st.session_state.gallery[view_cat]
    
    if images_list:
        st.write(f"Showing latest patterns in **{view_cat}**:")
        for img_url in images_list:
            st.image(img_url, use_container_width=True)
    else:
        st.info(f"💡 Abhi **{view_cat}** folder me koi photo nahi hai. Sidebar me 'Upload New Designs' par jaakar naye clothes ki photos add karein!")
