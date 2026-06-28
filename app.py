import streamlit as st
import requests
import base64

# Page Setup for Mobile/PC view
st.set_page_config(page_title="Boutique Design Hub", layout="centered")

st.title("👗 Premium Boutique Design Showcase 📐")
st.write("Apne customers ko latest designs dikhayein aur mobile se live photos manage karein!")

# 🔑 --- IMGBB FREE API STORAGE CONFIG ---
# Niche jo IMGBB_API_KEY likha hai, usme 'YOUR_API_KEY_HERE' mita kar apni asli key paste karein
IMGBB_API_KEY = "ed2197353c745545de89141360d71129"

# --- 📂 BOUTIQUE FOLDERS LIST ---
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

# Session State to store image URLs permanently for this session
if "gallery" not in st.session_state:
    st.session_state.gallery = {cat: [] for cat in categories}

# Sidebar Navigation for Admin (Upload) and Customer (View)
st.sidebar.header("🛠️ Boutique Control Panel")
app_mode = st.sidebar.radio("Go to:", ["👀 View Design Gallery", "📤 Upload New Designs"])

# ==========================================
# MODE 1: UPLOAD DESIGNS (ADMIN MODE)
# ==========================================
if app_mode == "📤 Upload New Designs":
    st.header("📤 Upload Latest Boutique Designs")
    
    selected_cat = st.selectbox("Kaun se folder me photo daalni hai?", categories)
    uploaded_file = st.file_uploader("Mobile Camera ya Gallery se Photo chuno:", type=["jpg", "png", "jpeg"])
    
    if st.button("Upload to Cloud 🚀") and uploaded_file is not None:
        with st.spinner("Photo cloud me save ho rahi hai..."):
            try:
                # Convert image to base64 for ImgBB API
                img_bytes = uploaded_file.read()
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                # Post request to ImgBB free server
                payload = {
                    "key": IMGBB_API_KEY,
                    "image": base64_image
                }
                response = requests.post("https://imgbb.com", data=payload)
                res_data = response.json()
                
                if response.status_code == 200:
                    image_url = res_data["data"]["url"]
                    # Add to session state category
                    st.session_state.gallery[selected_cat].append(image_url)
                    st.success(f"✅ Photo successfully **{selected_cat}** folder me add ho gayi!")
                else:
                    st.error(f"Upload fail hua: {res_data['error']['message']}")
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# MODE 2: VIEW GALLERY (CUSTOMER MODE)
# ==========================================
else:
    st.header("🖼️ Explore Design Collections")
    view_cat = st.selectbox("Select Category to View:", categories)
    
    st.markdown("---")
    images_list = st.session_state.gallery[view_cat]
    
    if images_list:
        st.write(f"Showing latest patterns in **{view_cat}**:")
        # Grid layout for mobile responsiveness
        for img_url in images_list:
            st.image(img_url, use_container_width=True)
    else:
        st.info(f"💡 Abhi **{view_cat}** folder me koi photo nahi hai. Sidebar me jaakar 'Upload New Designs' se photo add karein!")
