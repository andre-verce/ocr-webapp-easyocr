import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import time

# --- Configurazione pagina ---
st.set_page_config(page_title="OCR Web App (EasyOCR)", page_icon="🔠", layout="centered")

# --- Stile CSS personalizzato ---
st.markdown("""
    <style>
    div.stButton > button, .stDownloadButton > button {
        display: block;
        margin: 0.75em auto;
        width: 80%;
        height: 3em;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titolo ---
st.title("🔠 OCR Web App — EasyOCR Edition")
st.write("Carica un'immagine e rileva automaticamente il testo in diverse lingue.")

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
    st.image(image, caption="Immagine caricata", use_container_width=True)

    if st.button("🔍 Analizza immagine"):
        st.write("⏳ Analisi in corso...")
        progress_bar = st.progress(0)

        # --- Inizializza OCR ---
        reader = easyocr.Reader(selected_langs)

        # --- Simuliamo la progressione con piccoli step ---
        steps = 5
        for i in range(steps):
            time.sleep(0.2)  # piccola pausa per animare la progressione
            progress_bar.progress((i+1)/steps)

        # --- Esegui OCR ---
        result = reader.readtext(np.array(image), detail=0)

        text = "\n".join(result).strip() or "[Nessun testo riconosciuto]"

        st.success("✅ Analisi completata!")

        # --- Conteggio parole e caratteri ---
        words_count = len(text.split())
        chars_count = len(text)

        st.text_area("📝 Testo riconosciuto:", text, height=300)
        st.write(f"**Parole riconosciute:** {words_count}  |  **Caratteri totali:** {chars_count}")

        # --- Pulsante download ---
        st.download_button(
            label="💾 Scarica risultato come .txt",
            data=text,
            file_name="risultato_ocr.txt",
            mime="text/plain"
        )
