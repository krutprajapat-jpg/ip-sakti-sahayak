import streamlit as st
from utils import analyze_formulation

# Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium UI, Glassmorphism, and Mobile Responsiveness
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hide Streamlit Default Header and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glassmorphism Container Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* Custom Header Styling */
    .main-title {
        font-size: 2.2rem;
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
        margin-bottom: 25px;
    }

    /* Custom Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }

    /* Input Fields Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6);
        color: #f8fafc;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }

    /* Responsive adjustments for Mobile */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.6rem;
        }
        .glass-card {
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.markdown('<div class="main-title">⚖️ IP-SAKTI Sahayak</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered Traditional Formulation & Patent Compliance Analyzer (Sec 3(p))</div>', unsafe_allow_html=True)

# Main Form Container inside Glassmorphism Card
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    form_name = st.text_input("🌿 Formulation Name", placeholder="e.g., AyurImmune Kwath")
    ingredients = st.text_area("🧪 Key Ingredients", placeholder="List herbs, minerals, or components separated by commas...")
    process = st.text_area("⚙️ Manufacturing Process / Unique Benefit", placeholder="Describe unique extraction methods or novel modifications...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze Compliance & Patent Scope")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Execution & Results
if analyze_btn:
    if not form_name or not ingredients:
        st.warning("⚠️ Please fill in at least the Formulation Name and Ingredients to proceed.")
    else:
        with st.spinner("🔍 Consulting AI Patent Examiner & Scanning TKDL Database..."):
            report = analyze_formulation(form_name, ingredients, process)
        
        # Results Display Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Evaluation Report")
        st.markdown(report)
        
        # Download Option for Report
        st.download_button(
            label="📥 Download Official Legal Report (TXT)",
            data=report,
            file_name=f"{form_name.replace(' ', '_')}_patent_report.txt",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)