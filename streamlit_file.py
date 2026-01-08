import streamlit as st
import requests
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Load .env
# --------------------------------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("❌ OPENROUTER_API_KEY not found in .env file")
    st.stop()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Agricultural Disease Advisory AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Agricultural Disease Advisory System")
st.write(
    "Scientifically accurate, safe, and extension-grade crop disease guidance "
    "powered by NVIDIA Nemotron via OpenRouter."
)

# --------------------------------------------------
# OpenRouter API Call
# --------------------------------------------------
def generate_agri_response(plant, disease):
    prompt = f"""
You are an agricultural expert specializing in plant pathology, crop nutrition, and safe farm management.
Your job is to provide accurate, scientifically correct, and legally safe advice.

Plant: {plant}
Issue: {disease}

Your response MUST follow this structure clearly and must be 100% accurate:

### 1. About the Disease
- Explain what the disease is and identify the correct pathogen type
- Describe how it spreads

### 2. Symptoms
- Leaves
- Stems
- Roots
- Fruit (only if applicable)
- Tubers/roots if relevant

### 3. Safe & Legal Treatment Options
- Copper-based fungicides
- Mancozeb
- Chlorothalonil
- Sulfur (if relevant)
- Biological controls
- Cultural practices

Rules:
- NO dosages
- NO banned chemicals
- Fertilizers do NOT cure disease

### 4. Prevention
- Resistant varieties
- Crop rotation
- Spacing & airflow
- Moisture control
- Drip irrigation
- Field sanitation

### 5. Nutrient Requirements
Explain N, P, K, Ca, Mg, S and micronutrients.

### 6. Fertilizer Recommendations (No Dosages)
- Chemical
- Organic
- Biofertilizers

### 7. Additional Good Practices
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",   # required by OpenRouter
            "X-Title": "Agricultural Disease Advisory AI"
        },
        json={
            "model": "nvidia/nemotron-3-nano-30b-a3b:free",
            "messages": [
                {"role": "system", "content": "You are a strict agricultural science expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 900
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]

# --------------------------------------------------
# UI Inputs
# --------------------------------------------------
with st.form("agri_form"):
    plant = st.text_input("🌾 Crop / Plant Name", placeholder="e.g. Potato")
    disease = st.text_input("🦠 Disease / Problem", placeholder="e.g. Late Blight")
    submitted = st.form_submit_button("Generate Advisory")

# --------------------------------------------------
# Output
# --------------------------------------------------
if submitted:
    if not plant or not disease:
        st.warning("Please enter both plant and disease.")
    else:
        with st.spinner("Generating scientifically accurate guidance..."):
            try:
                result = generate_agri_response(plant, disease)
                st.markdown("## 📋 Advisory Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
