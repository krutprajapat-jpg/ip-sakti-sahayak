import streamlit as st
from groq import Groq

# Initialize Groq Client using Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

@st.cache_data(show_spinner=False)
def analyze_formulation(domain, name, description, process):
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
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq API: {str(e)}" 