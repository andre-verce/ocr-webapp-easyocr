import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# --- Configurazione pagina ---
st.set_page_config(page_title="OCR Web App (EasyOCR)", page_icon="🔠", layout="centered")

# --- Stile CSS personalizzato ---
st.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
        width: 60%;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titolo ---
st.title("🧠 OCR Web App — EasyOCR Edition")
st.write("Carica un'immagine e rileva automaticamente il testo in diverse lingue (tutto direttamente nel browser Streamlit Cloud).")

# --- Upload immagine ---
uploaded_file = st.file_uploader("📁 Carica un'immagine", type=["png", "jpg", "jpeg"])

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

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Analizza"):
            st.write("⏳ Analisi in corso...")

            # Inizializza il lettore EasyOCR con le lingue scelte
            reader = easyocr.Reader(selected_langs)
            result = reader.readtext(np.array(image), detail=0)

            text = "\n".join(result)
            if not text.strip():
                text = "[Nessun testo riconosciuto]"

            st.success("✅ Analisi completata!")
            st.text_area("📝 Testo riconosciuto:", text, height=300)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.download_button(
                    label="💾 Scarica risultato come .txt",
                    data=text,
                    file_name="risultato_ocr.txt",
                    mime="text/plain"
                )
