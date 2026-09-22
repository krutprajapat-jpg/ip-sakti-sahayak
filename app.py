import streamlit as st
import random
import smtplib
from email.message import EmailMessage
import re
from utils import analyze_formulation

# Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak | Ministry of Ayush",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Government Portal UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;600;700&display=swap');

    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .clean-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        padding: 32px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #0f172a !important;
        font-weight: 700;
    }

    p, span, label, .stMarkdown {
        color: #334155 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .portal-subtitle {
        color: #475569 !important;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 24px;
    }

    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    input, textarea, select {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-weight: 600 !important;
    }

    .stSelectbox>div>div>div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }

    .stButton>button, div.stFormSubmitButton>button {
        width: 100%;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Fixed Function to Send Real Email OTP using Gmail SMTP
def send_email_otp(receiver_email, otp_code):
    SENDER_EMAIL = st.secrets["SENDER_EMAIL"]  
    SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]  
    
    msg = EmailMessage()
    msg['Subject'] = "IP-SAKTI Sahayak - Login Verification Code (OTP)"
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    
    msg.set_content(f"""
    Namaste,
    
    Aapka IP-SAKTI Sahayak portal login verification code (OTP) yeh hai: {otp_code}
    
    Yeh code 10 minutes ke liye valid hai. Kripya ise kisi ke sath share na karein.
    
    Regards,
    Ministry of Ayush Team
    """)
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return str(e)

# Session State Initializations
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
    st.session_state.generated_otp = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Email validation regex pattern
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

# --- AUTHENTICATION SCREEN ---
if not st.session_state.logged_in:
    col_center1, col_main, col_center2 = st.columns([1, 1.4, 1])
    
    with col_main:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 5px; justify-content: center;">
            <div style="background: linear-gradient(135deg, #059669 0%, #2563eb 100%); padding: 12px; border-radius: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                    <path d="M9 12l2 2 4-4"></path>
                </svg>
            </div>
            <div>
                <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2.1rem; background: linear-gradient(135deg, #047857 0%, #2563eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">IP-SAKTI Sahayak</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="portal-subtitle" style="text-align: center;">Ministry of Ayush • Official Email Security Portal</p>', unsafe_allow_html=True)
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        
        st.markdown("#### ✉️ Enter Email Address")
        st.markdown("<p style='font-size: 0.9rem; color: #64748b;'>A secure verification code (OTP) will be sent to your email inbox.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        user_email = st.text_input("Email Address", placeholder="e.g., name@example.com", value=st.session_state.user_email, key="email_input")
        
        if user_email and not is_valid_email(user_email):
            st.error("⚠️ Kripya ek valid email address enter karein (jaise: abc@gmail.com).")
        
        if not st.session_state.otp_sent:
            if st.button("Send Email Verification Code"):
                if is_valid_email(user_email.strip()):
                    st.session_state.user_email = user_email.strip()
                    st.session_state.generated_otp = str(random.randint(1000, 9999))
                    
                    with st.spinner("📧 Sending secure OTP to your email..."):
                        res = send_email_otp(st.session_state.user_email, st.session_state.generated_otp)
                        
                    if res is True:
                        st.session_state.otp_sent = True
                        st.success(f"✅ OTP successfully sent to {st.session_state.user_email}!")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ SMTP Connection note: [{res}]. For testing right now, your generated OTP is: **{st.session_state.generated_otp}**")
                        st.session_state.otp_sent = True
                        st.rerun()
                else:
                    st.warning("⚠️ Kripya pehle ek valid email address enter karein.")
        else:
            st.info(f"📩 Verification code sent to **{st.session_state.user_email}**.")
            
            entered_otp = st.text_input("Enter 4-digit OTP", placeholder="", max_chars=4, key="otp_input")
            
            if entered_otp and not entered_otp.isdigit():
                st.error("⚠️ OTP mein kewal numbers hone chahiye.")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                verify_btn = st.button("Verify & Login")
            with col_b2:
                resend_btn = st.button("Resend Code")
                
            if verify_btn:
                if entered_otp.strip() == st.session_state.generated_otp:
                    st.session_state.logged_in = True
                    st.success("OTP Verified Successfully! Launching portal...")
                    st.rerun()
                else:
                    st.error("❌ Galat OTP enter kiya gaya hai. Dubara check karein.")
                    
            if resend_btn:
                st.session_state.generated_otp = str(random.randint(1000, 9999))
                send_email_otp(st.session_state.user_email, st.session_state.generated_otp)
                st.info(f"📩 Naya OTP bhej diya gaya hai. [Testing OTP]: **{st.session_state.generated_otp}**")
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
            <div style="background: linear-gradient(135deg, #059669 0%, #2563eb 100%); padding: 8px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                    <path d="M9 12l2 2 4-4"></path>
                </svg>
            </div>
            <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.3rem; background: linear-gradient(135deg, #047857 0%, #2563eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">IP-SAKTI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='color: #475569; font-size: 0.85rem;'>Logged in: {st.session_state.user_email}</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🛠️ Workspace Tools")
        st.markdown("- 🔬 Formulation Patent Audit")
        st.markdown("- 📚 TKDL Prior Art Scanner")
        st.markdown("- ⚖️ Section 3(d) / 3(p) Validator")
        st.markdown("---")
        if st.button("🚪 Secure Logout"):
            st.session_state.logged_in = False
            st.session_state.otp_sent = False
            st.rerun()

    col_h1, col_h2 = st.columns([8, 2])
    with col_h1:
        st.markdown("# 🔬 Advanced Pharma & Traditional IP Audit Engine")
        st.markdown("<p class='portal-subtitle'>Official Prior Art Verification & Patent Compliance Suite</p>", unsafe_allow_html=True)
    with col_h2:
        st.markdown("<div style='text-align: right; padding-top: 10px;'><span style='background: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;'>🟢 System Online</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    
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
    
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        innov_name = st.text_input("💡 Formulation / Drug Trade Name", placeholder="e.g., Nano-Curcumin Suspension")
    with col_i2:
        category_type = st.selectbox("📂 Patent Filing Category", ["New Chemical Entity (NCE)", "Herbal/Traditional Formulation", "Novel Drug Delivery System (NDDS)", "Synergistic Combination"])

    description = st.text_area("🧪 Active Pharmaceutical Ingredients (APIs) / Excipients / Herbs", placeholder="List core active molecules...")
    process = st.text_area("⚙️ Manufacturing Process / Bioavailability Advantage", placeholder="Describe synthesis pathway...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Run Comprehensive Medical Patent & Efficacy Audit")
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not innov_name or not description:
            st.warning("⚠️ Please fill in at least the Formulation Name and Active Ingredients to proceed.")
        else:
            with st.spinner("🔍 Scanning Global Pharmacopoeia & Traditional Knowledge Digital Databases..."):
                report = analyze_formulation(domain, innov_name, description, process)
            
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Official Pharmaceutical IP Evaluation Report")
            st.markdown(report)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Official Legal Report (TXT)",
                data=report,
                file_name=f"{innov_name.replace(' ', '_')}_pharma_audit.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)