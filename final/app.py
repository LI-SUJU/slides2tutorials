import streamlit as st
from cc_fin_v1_0 import (
    clean_text,
    remove_repetitions,
    summarize_text,
    generate_narrative,
    generate_combined_voice_over,
    generate_formatted_pdf,
)
from PyPDF2 import PdfReader
import os

# Create output directories
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_pdf(file):
    try:
        # Save uploaded PDF
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # Read and process PDF
        pdf_reader = PdfReader(file_path)
        narratives = []
        pages = pdf_reader.pages

        for i, page in enumerate(pages, start=1):
            raw_text = page.extract_text()
            clean_page_text = clean_text(raw_text)
            deduplicated_text = remove_repetitions(clean_page_text)
            summary = summarize_text(deduplicated_text)
            narrative = generate_narrative(summary)
            narratives.append(f"Page {i}:\n{narrative}")

        # Generate outputs
        combined_audio_path = os.path.join(OUTPUT_FOLDER, "combined_voiceover.mp3")
        generate_combined_voice_over(narratives, output_path=combined_audio_path)

        pdf_output_path = os.path.join(OUTPUT_FOLDER, "Generated_Narratives.pdf")
        generate_formatted_pdf(narratives, output_file=pdf_output_path)

        return combined_audio_path, pdf_output_path, narratives

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {str(e)}")
        return None, None, None

# Streamlit App
st.title("Lecture Slides to Tutorial Generator")
st.write("Upload your lecture slides (PDF) to generate narrated audio and formatted PDF.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.write("Processing your file...")
    audio_path, pdf_path, generated_narratives = process_pdf(uploaded_file)

    if audio_path and pdf_path:
        # Display Results
        st.success("Processing complete!")
        st.write("### Download Generated Outputs")
        st.download_button(
            label="Download Generated PDF",
            data=open(pdf_path, "rb").read(),
            file_name="Generated_Narratives.pdf",
            mime="application/pdf",
        )
        st.download_button(
            label="Download Narrated Audio",
            data=open(audio_path, "rb").read(),
            file_name="Generated_Audio.mp3",
            mime="audio/mpeg",
        )

        # Display Generated Narratives
        st.write("### Narratives")
        for i, narrative in enumerate(generated_narratives, start=1):
            st.write(f"**Page {i}:** {narrative}")
