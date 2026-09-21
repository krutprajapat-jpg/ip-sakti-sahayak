import streamlit as st
import random
from utils import analyze_formulation

# Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak - Secure Portal",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Animations & Glassmorphism
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 5px rgba(99, 102, 241, 0.2); }
        50% { box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.5); }
        100% { box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 5px rgba(99, 102, 241, 0.2); }
    }

    .glass-card {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 30px;
        border-radius: 20px;
        animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards, glowPulse 4s infinite ease-in-out;
        margin-bottom: 20px;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    .stButton>button, div.stFormSubmitButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton>button:hover, div.stFormSubmitButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.7);
        transform: translateY(-3px);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.7);
        color: #f8fafc;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 12px;
    }

    @media (max-width: 768px) {
        .main-title { font-size: 1.8rem; }
        .glass-card { padding: 20px; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Generate a new random captcha question if it doesn't exist in session
if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 10)
    st.session_state.captcha_num2 = random.randint(1, 10)
    st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2

# --- LOGIN & CAPTCHA SCREEN ---
if not st.session_state.logged_in:
    st.markdown('<div class="main-title">🔐 IP-SAKTI Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Next-Gen Secure Access & Verification</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username (admin)")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            
            st.markdown("---")
            st.markdown("🛡️ **Security Verification (Dynamic Captcha)**")
            
            # Display dynamic random question
            q_text = f"Please solve: What is {st.session_state.captcha_num1} + {st.session_state.captcha_num2} ?"
            st.text(q_text)
            
            captcha_input = st.text_input("Enter Answer", placeholder="Type answer...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("🔓 Secure Login")
            
            if submit_login:
                if username == "admin" and password == "sakti123":
                    if captcha_input.strip() == str(st.session_state.captcha_ans):
                        st.session_state.logged_in = True
                        # Clear captcha state after successful login
                        del st.session_state.captcha_num1
                        del st.session_state.captcha_num2
                        del st.session_state.captcha_ans
                        st.rerun()
                    else:
                        st.error("❌ Incorrect Captcha answer! A new captcha has been generated.")
                        # Reset captcha on failure for security
                        st.session_state.captcha_num1 = random.randint(1, 10)
                        st.session_state.captcha_num2 = random.randint(1, 10)
                        st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2
                else:
                    st.error("❌ Invalid Username or Password! (Use admin / sakti123)")
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN APP DASHBOARD ---
else:
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown('<div class="main-title">⚖️ IP-SAKTI Sahayak</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">AI-Powered Traditional Formulation & Patent Compliance Analyzer</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            # Generate fresh captcha for next login
            st.session_state.captcha_num1 = random.randint(1, 10)
            st.session_state.captcha_num2 = random.randint(1, 10)
            st.session_state.captcha_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2
            st.rerun()

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        form_name = st.text_input("🌿 Formulation Name", placeholder="e.g., AyurImmune Kwath")
        ingredients = st.text_area("🧪 Key Ingredients", placeholder="List components separated by commas...")
        process = st.text_area("⚙️ Manufacturing Process / Unique Benefit", placeholder="Describe unique methods...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze Compliance & Patent Scope")
        
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not form_name or not ingredients:
            st.warning("⚠️ Please fill in at least the Formulation Name and Ingredients.")
        else:
            with st.spinner("🔍 Consulting AI Patent Examiner & Scanning TKDL Database..."):
                report = analyze_formulation(form_name, ingredients, process)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Evaluation Report")
            st.markdown(report)
            
            st.download_button(
                label="📥 Download Official Legal Report (TXT)",
                data=report,
                file_name=f"{form_name.replace(' ', '_')}_patent_report.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)