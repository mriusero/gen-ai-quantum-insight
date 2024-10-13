from typing import Tuple

import streamlit as st

from .processing.preprocessing import handle_document_loading
from .processing.preprocessor import DocumentProcessor
from .qa_system.qa_system import QASystem
from .utilities.helper import VECTOR_STORE_FILE, load_processed_pdfs, display_files

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource
def load_models(hg_api_key: str, debug: bool = False) -> Tuple[DocumentProcessor, QASystem]:
    """Load and cache document processor and QA system models."""
    return (
        DocumentProcessor(
            debug=debug,
            embedding_model=EMBEDDING_MODEL
        ),
        QASystem(
            api_key=hg_api_key,
            debug=debug,
            model_name=MODEL_NAME,
            embedding_model=EMBEDDING_MODEL,
            vector_store_file=VECTOR_STORE_FILE
        )
    )

def run_assistance(hg_api_key: str, debug: bool = False) -> None:
    """Main logic for the research assistant app, handling document processing and QA system."""
    st.title("Research Assistant")
    document_processing, qa_system = load_models(hg_api_key, debug)

    pdf_urls = st.session_state.get('data', {}).get('pdf_link', [])[:300]
    processed_pdfs = load_processed_pdfs()

    new_pdfs = [url for url in pdf_urls if url not in processed_pdfs]
    already_processed = [url for url in pdf_urls if url in processed_pdfs]

    display_files(new_pdfs, already_processed)

    if new_pdfs:
        if st.button("Vectorize Documents"):
            handle_document_loading(new_pdfs, document_processing, processed_pdfs, debug)
    else:
        st.info("Vector store already up to date")

    qa_system.initialize_ui()
