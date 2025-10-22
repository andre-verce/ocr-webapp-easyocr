import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# --- Configurazione pagina ---
st.set_page_config(page_title="OCR Web App (EasyOCR)", page_icon="🔠", layout="centered")

# --- Stile CSS personalizzato ---
st.markdown("""
    <style>
    /* Centra e allarga i pulsanti principali */
    div.stButton > button {
        display: block;
        margin: 0.75em auto;
        width: 80%;
        height: 3em;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px !important;
    }
    /* Allarga il pulsante di download */
    .stDownloadButton > button {
        display: block;
        margin: 1em auto;
        width: 80%;
        height: 3em;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titolo ---
st.title("🔠 OCR Web App — EasyOCR Edition")
st.write("Carica un'immagine e rileva automaticamente il testo in diverse lingue (direttamente nel browser Streamlit Cloud).")

# --- Upload immagine ---
uploaded_file = st.file_uploader("📁 Carica un'immagine (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

# --- Scelta lingue OCR ---
available_langs = ['en', 'it', 'fr', 'es', 'de', 'pt']
selected_langs = st.multiselect(
    "🌐 Seleziona le lingue per l'OCR",
    options=available_langs,
    default=['en', 'it']
)

# --- Analisi immagine ---
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    # Pulsante "Analizza" centrato e largo
    if st.button("🔍 Analizza immagine"):
        st.write("⏳ Analisi in corso...")
        reader = easyocr.Reader(selected_langs)
        result = reader.readtext(np.array(image), detail=0)

        text = "\n".join(result).strip() or "[Nessun testo riconosciuto]"

        st.success("✅ Analisi completata!")
        st.text_area("📝 Testo riconosciuto:", text, height=300)

        # Pulsante di download centrato e largo
        st.download_button(
            label="💾 Scarica risultato come .txt",
            data=text,
            file_name="risultato_ocr.txt",
            mime="text/plain"
        )
