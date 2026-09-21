import streamlit as st
import random
import json
import os
from utils import analyze_formulation

# Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak - Pharma IP Portal",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Next-Gen Medical/Pharma Vibe & WhatsApp-style Entry Animation
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #064e3b 0%, #022c22 60%, #021a14 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background-attachment: fixed;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @keyframes appLaunch {
        0% { opacity: 0; transform: scale(0.92) translateY(30px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    @keyframes glowBorder {
        0% { border-color: rgba(52, 211, 153, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        50% { border-color: rgba(16, 185, 129, 0.6); box-shadow: 0 15px 45px rgba(52, 211, 153, 0.25); }
        100% { border-color: rgba(52, 211, 153, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
    }

    .glass-card {
        background: rgba(2, 44, 34, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(52, 211, 153, 0.2);
        padding: 32px;
        border-radius: 24px;
        animation: appLaunch 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards, glowBorder 5s infinite ease-in-out;
        margin-bottom: 25px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 28px;
        font-weight: 400;
    }

    .stButton>button, div.stFormSubmitButton>button {
        width: 100%;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        font-weight: 600;
        padding: 0.8rem 1rem;
        border-radius: 14px;
        border: none;
        box-shadow: 0 4px 20px rgba(5, 150, 105, 0.45);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton>button:hover, div.stFormSubmitButton>button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.7);
        transform: translateY(-2px);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(6, 78, 59, 0.6) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(52, 211, 153, 0.25) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    @media (max-width: 768px) {
        .main-title { font-size: 1.8rem; }
        .glass-card { padding: 20px; }
    }
    </style>
""", unsafe_allow_html=True)

USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except:
            return {"admin": "sakti123"}
    return {"admin": "sakti123"}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 10)
    st.session_state.captcha_num2 = random.randint(1, 10)
    st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2

# --- AUTHENTICATION SCREEN ---
if not st.session_state.logged_in:
    st.markdown('<div class="main-title">💊 IP-SAKTI Sahayak</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Advanced Pharmaceutical & Medical IP Compliance Portal</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔓 Secure Login", "📝 Create New Account"])
        
        with tab_login:
            with st.form("login_form"):
                l_user = st.text_input("👤 Username", placeholder="Enter your username", key="l_user")
                l_pass = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="l_pass")
                
                st.markdown("---")
                st.markdown(f"🛡️ **Security Check:** What is {st.session_state.captcha_num1} + {st.session_state.captcha_num2} ?")
                l_captcha = st.text_input("Enter Answer", placeholder="Type answer...", key="l_cap")
                
                st.markdown("<br>", unsafe_allow_html=True)
                login_submit = st.form_submit_button("Access Portal")
                
                if login_submit:
                    users_db = load_users()
                    if l_user in users_db and users_db[l_user] == l_pass:
                        if l_captcha.strip() == str(st.session_state.captcha_ans):
                            st.session_state.logged_in = True
                            st.session_state.username = l_user
                            st.rerun()
                        else:
                            st.error("❌ Incorrect Captcha answer! A new code has been generated.")
                            st.session_state.captcha_num1 = random.randint(1, 10)
                            st.session_state.captcha_num2 = random.randint(1, 10)
                            st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2
                    else:
                        st.error("❌ Invalid Username or Password!")

        with tab_register:
            with st.form("register_form"):
                r_user = st.text_input("👤 Choose Username", placeholder="Create a unique username", key="r_user")
                r_pass = st.text_input("🔑 Choose Password", type="password", placeholder="Create a password", key="r_pass")
                r_pass_confirm = st.text_input("🔑 Confirm Password", type="password", placeholder="Re-enter password", key="r_pass_confirm")
                
                st.markdown("<br>", unsafe_allow_html=True)
                register_submit = st.form_submit_button("Register & Login Instantly")
                
                if register_submit:
                    users_db = load_users()
                    if not r_user or not r_pass:
                        st.warning("⚠️ Please fill in all fields.")
                    elif r_user in users_db:
                        st.error("❌ Username already exists! Choose another one.")
                    elif r_pass != r_pass_confirm:
                        st.error("❌ Passwords do not match!")
                    else:
                        users_db[r_user] = r_pass
                        save_users(users_db)
                        st.session_state.logged_in = True
                        st.session_state.username = r_user
                        st.success("✅ Account created successfully! Launching portal...")
                        st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN PHARMA DASHBOARD ---
else:
    col1, col2 = st.columns([7, 3])
    with col1:
        st.markdown('<div class="main-title">💊 IP-SAKTI Sahayak</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">Welcome, <b>{st.session_state.username}</b> | Multi-Pharmacy Patent Examiner</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.captcha_num1 = random.randint(1, 10)
            st.session_state.captcha_num2 = random.randint(1, 10)
            st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2
            st.rerun()

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        domain = st.selectbox(
            "🔬 Select Medical / Pharmacy Branch", 
            [
                "💊 Allopathic & Modern Pharmaceuticals (APIs, Synthetic Drugs & Formulations)", 
                "🌿 Ayurveda & Herbal Pharmacy (Traditional Knowledge / TKDL / Sec 3(p))", 
                "⚪ Homeopathy Pharmacy (Mother Tinctures, Dilutions & Potencies)", 
                "🍃 Unani & Siddha Traditional Medicine Systems", 
                "🧬 Nutraceuticals, Biologics & Dietary Supplements"
            ]
        )
        
        innov_name = st.text_input("💡 Formulation / Drug Trade Name", placeholder="e.g., Nano-Curcumin Suspension / Extended-Release Metformin Complex")
        description = st.text_area("🧪 Active Pharmaceutical Ingredients (APIs) / Excipients / Herbs", placeholder="List core active molecules, chemical salts, herbal extracts, or excipients...")
        process = st.text_area("⚙️ Manufacturing Process / Novel Drug Delivery System (NDDS) / Bioavailability Advantage", placeholder="Describe synthesis pathway, particle size reduction, sustained-release mechanism, or enhanced efficacy...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Run Comprehensive Medical Patent & Efficacy Audit")
        
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not innov_name or not description:
            st.warning("⚠️ Please fill in at least the Formulation Name and Ingredients to proceed.")
        else:
            with st.spinner("🔍 Scanning Global Pharmacopoeia & Patent Prior Art Databases..."):
                report = analyze_formulation(domain, innov_name, description, process)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Official Pharmaceutical IP Evaluation Report")
            st.markdown(report)
            
            st.download_button(
                label="📥 Download Official Legal Report (TXT)",
                data=report,
                file_name=f"{innov_name.replace(' ', '_')}_pharma_audit.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)