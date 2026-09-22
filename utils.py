from langchain_community.llms import Ollama

def analyze_formulation(domain, innov_name, description, process):
    try:
        # Initialize local Llama 3 model via Ollama
        llm = Ollama(model="llama3")
        
        prompt = f"""
        You are 'IP-SAKTI Sahayak', an advanced AI assistant for Pharmaceutical and Medical IP Compliance (Ministry of Ayush / Patent Office).
        Analyze the following formulation and provide a structured patent compliance and prior art evaluation report.
        
        Medical Domain: {domain}
        Formulation/Trade Name: {innov_name}
        APIs/Ingredients/Excipients: {description}
        Manufacturing Process / Novelty: {process}
        
        Provide a detailed evaluation covering:
        1. Patentability Analysis (Novelty, Non-obviousness, Industrial applicability)
        2. Section 3(d) / Section 3(p) Traditional Knowledge / Ayush Compliance check
        3. Potential Prior Art risks
        4. Recommendations for filing
        """
        
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"Error connecting to local Ollama model: {str(e)}\n\nMake sure Ollama app/background service is running!"