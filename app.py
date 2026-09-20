import streamlit as st
import time
from utils import analyze_formulation

# Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak | Legal-Tech Compliance",
    page_icon="⚖️",
    layout="wide"
)

# Initialize Session State for Login and App Flow
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'splash_done' not in st.session_state:
    st.session_state['splash_done'] = False

# --- 1. SPLASH SCREEN ANIMATION ---
if not st.session_state['splash_done']:
    st.markdown("""
        <style>
        .splash-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            text-align: center;
        }
        .splash-title {
            font-size: 3rem;
            color: #1E3A8A;
            font-weight: 800;
        }
        .splash-sub {
            font-size: 1.2rem;
            color: #4B5563;
        }
        </style>
        <div class="splash-container">
            <p class="splash-title">⚖️ IP-SAKTI Sahayak</p>
            <p class="splash-sub">Initializing AI Legal-Tech & TKDL Compliance Engine...</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simulate loading progress
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
        
    st.session_state['splash_done'] = True
    st.rerun()

# --- 2. LOGIN / ACCESS GATE ---
if not st.session_state['logged_in']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Secure Legal Portal Login")
        st.markdown("Enter your researcher or startup credentials to access the IP screening engine.")
        
        username = st.text_input("Username / Founder ID", placeholder="e.g., admin_sih")
        password = st.text_input("Access Password", type="password", placeholder="********")
        
        if st.button("Login to Dashboard", type="primary", use_container_width=True):
            if username and password:
                st.session_state['logged_in'] = True
                st.success("Login Successful! Redirecting...")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("Please enter valid login details.")
    st.stop()

# --- 3. MAIN APP DASHBOARD (After Login) ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar with Logout Option
top_col1, top_col2 = st.columns([8, 2])
with top_col1:
    st.markdown('<p class="main-header">⚖️ IP-SAKTI Sahayak</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Prior Art & Section 3(p) Compliance Screening Tool</p>', unsafe_allow_html=True)
with top_col2:
    if st.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

st.markdown("---")

# Sidebar for Inputs
st.sidebar.header("🌿 Formulation Input Panel")
form_name = st.sidebar.text_input("Formulation Name", "e.g., Herbal Skin Healing Ointment")
ingredients = st.sidebar.text_area("Key Ingredients & Proportions", "e.g., Chakramarden ext. 16%, Manjistha ext. 13%, Giloy ext. 20%")
process = st.sidebar.text_area("Manufacturing Process / Unique Benefit", "e.g., Special nano-emulsion extraction method for enhanced absorption.")

analyze_btn = st.sidebar.button("Run Compliance & Patent Filter", type="primary", use_container_width=True)

# Main Content Tabs
tab1, tab2, tab3 = st.tabs(["📊 Compliance Dashboard", "📜 Legal Framework (Sec 3p)", "ℹ️ About System"])

with tab1:
    if analyze_btn:
        if not form_name or not ingredients:
            st.warning("Please fill in the formulation name and ingredients in the sidebar!")
        else:
            with st.spinner("Scanning formulation against TKDL database and Section 3(p) rules..."):
                report_text = analyze_formulation(form_name, ingredients, process)
                st.session_state['last_report'] = report_text
                st.session_state['form_name'] = form_name
                
            st.success("Analysis Complete!")
            st.markdown("### 📋 Evaluation Report")
            st.markdown(report_text)
            
            st.markdown("---")
            st.download_button(
                label="📥 Download Official Legal Report (TXT)",
                data=report_text,
                file_name=f"{form_name.replace(' ', '_')}_IP_Sakti_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        if 'last_report' in st.session_state:
            st.markdown(f"### 📋 Evaluation Report for: {st.session_state.get('form_name', 'Formulation')}")
            st.markdown(st.session_state['last_report'])
            st.download_button(
                label="📥 Download Official Legal Report (TXT)",
                data=st.session_state['last_report'],
                file_name="IP_Sakti_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("👈 Enter your formulation details in the sidebar and click **'Run Compliance & Patent Filter'** to initiate scanning.")

with tab2:
    st.subheader("Understanding Section 3(p) of the Indian Patents Act")
    st.write("""
    * **Section 3(p)** states that traditional knowledge or aggregation/duplication of known properties of traditional components is **not patentable**.
    * **TKDL (Traditional Knowledge Digital Library)** acts as a repository preventing false patents on ancient formulations.
    * **IP-SAKTI Sahayak** automates this screening process for AYUSH startups and patent examiners.
    """)

with tab3:
    st.subheader("About System Architecture")
    st.write("""
    * **Domain:** Traditional Indian Systems of Medicine & IP Law.
    * **Tech Stack:** Python, Streamlit, Advanced Generative AI Models.
    * **Purpose:** Built for Smart India Hackathon (SIH) to streamline patent novelty checks.
    """)