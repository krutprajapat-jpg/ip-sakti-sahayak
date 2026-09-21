import streamlit as st
import google.generativeai as genai
import time

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

@st.cache_data(show_spinner=False)
def analyze_formulation(domain, name, description, process):
    model = genai.GenerativeModel('gemini-3.6-flash')
    
    prompt = f"""
    Act as a senior Global Pharmaceutical Patent Examiner and Intellectual Property (IP) Compliance Expert specializing in Medical & Pharmacy Patent Laws (including Indian Patents Act Sec 3(d) for efficacy, Sec 3(p) for traditional systems, US FDA/USPTO guidelines, and international drug patentability).
    
    Analyze the following medical/pharmaceutical innovation under the domain: {domain}
    - Formulation / Drug Name: {name}
    - Active Ingredients / Excipients / Chemical Composition: {description}
    - Manufacturing Process / Novel Drug Delivery System (NDDS) / Therapeutic Advantage: {process}
    
    Your task is to determine whether this medical formulation is non-patentable (due to mere admixture under Sec 3(e), lack of enhanced efficacy under Sec 3(d), or prior art) or if it possesses a genuine 'Inventive Step' / Novelty / Therapeutic Efficacy.
    
    Provide a structured, professional report with these exact headings:
    1. CLASSIFICATION STATUS: (Choose one: CONVENTIONAL / MERE ADMIXTURE (Non-Patentable) OR NOVEL PHARMACEUTICAL / INVENTIVE FORMULATION (Potential Patent Scope))
    2. CONFIDENCE SCORE: (Give a percentage, e.g., 88%)
    3. LEGAL & PRIOR ART INSIGHTS: (Detailed legal reasoning based on pharmaceutical patent standards, bioavailability, side-effect reduction, or drug delivery technology)
    4. STRATEGIC RECOMMENDATION FOR INVENTOR: (Actionable advice for drafting patent claims, clinical/lab data requirements, and overcoming statutory rejections)
    
    Keep the tone formal, medical-legal, sharp, and authoritative.
    """
    
    max_retries = 3
    wait_time = 5
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    wait_time *= 2
                    continue
            return f"Error connecting to Gemini API: {error_str}"
            
    return "Error: API rate limit exceeded. Please wait a minute and try again."