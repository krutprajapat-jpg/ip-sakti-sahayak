import streamlit as st
import google.generativeai as genai

# Streamlit secrets se API key secure tareeke se uthao
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

def analyze_formulation(name, ingredients, process):
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        prompt = f"""
        Act as an expert Indian Patent Office examiner and Ayurvedic compliance officer specializing in Section 3(p) of the Indian Patents Act and TKDL (Traditional Knowledge Digital Library) standards.
        
        Analyze the following traditional/herbal formulation:
        - Formulation Name: {name}
        - Key Ingredients: {ingredients}
        - Manufacturing Process / Unique Benefit: {process}
        
        Your task is to determine whether this formulation is purely classical (non-patentable under Section 3(p) due to existing prior art) or if it has a unique 'Inventive Step' / novel modification that could qualify for a patent.
        
        Provide a structured, professional report with the following exact headings:
        1. CLASSIFICATION STATUS: (Choose one: CLASSICAL / TRADITIONAL (Non-Patentable) OR NOVEL / MODIFIED (Potential Patent Scope))
        2. CONFIDENCE SCORE: (Give a percentage, e.g., 85%)
        3. SECTION 3(p) & TKDL COMPLIANCE INSIGHTS: (Detailed legal reasoning regarding prior art, traditional texts, and novelty)
        4. STRATEGIC RECOMMENDATION FOR FOUNDER: (Actionable advice for filing or modifying the formulation)
        
        Keep the tone formal, legal, and authoritative.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"