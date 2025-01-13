import streamlit as st
import os
from pathlib import Path
from cc_fin_v1_0 import (
    generate_combined_voice_over,
    generate_formatted_pdf,
    clean_text,
    remove_repetitions,
    summarize_text,
    generate_narrative,
)
from PyPDF2 import PdfReader

# Streamlit App
st.title("Lecture Slide to Tutorial Generator")

# Upload section
uploaded_file = st.file_uploader("Upload your lecture slides (PDF)", type=["pdf"])

# User options
st.sidebar.header("Customization Options")
knowledge_level = st.sidebar.selectbox(
    "Knowledge Level", ["Beginner", "Medium", "Advanced", "Expert"]
)
voice_gender = st.sidebar.radio("Voice Gender", ["Male", "Female"])
humor = st.sidebar.checkbox("Add Humor")
detail_level = st.sidebar.slider(
    "Detail Level (Duration)", 1, 10, 5, help="Adjust the level of detail for the tutorial."
)

if uploaded_file:
    # Save uploaded file temporarily
    input_path = Path("temp") / uploaded_file.name
    input_path.parent.mkdir(exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Generate Audio Tutorial and PDF"):
        st.info("Processing... This may take a few minutes.")

        try:
            # Extract text from PDF
            reader = PdfReader(input_path)
            pages = [page.extract_text() for page in reader.pages]

            narratives = []
            for i, page_text in enumerate(pages, start=1):
                # Cleaning and preprocessing
                clean_page_text = clean_text(page_text)
                deduplicated_text = remove_repetitions(clean_page_text)

                # Summarize text
                summary = summarize_text(deduplicated_text)

                # Generate narrative with user preferences
                narrative_prompt = (
                    f"Please explain this content in a {voice_gender.lower()} voice. "
                    f"Include {'some humor' if humor else 'no humor'}, and make it "
                    f"{'detailed and thorough' if detail_level > 5 else 'concise'}. "
                    f"The audience has a {knowledge_level.lower()} level of knowledge. "
                    f"Content:\n\n{summary}"
                )
                narrative = generate_narrative(
                    narrative_prompt, voice_gender, humor, detail_level
                )
                narratives.append(f"Page {i}:\n{narrative}")

            # Generate output files
            audio_path = "./outputs/output_audio_tutorial.mp3"
            pdf_path = "./outputs/output_tutorial.pdf"

            generate_combined_voice_over(narratives, output_path=audio_path)
            generate_formatted_pdf(narratives, output_file=pdf_path)

            st.success("Generation Complete!")
            st.markdown(f"### [Download Audio Tutorial](./{audio_path})")
            st.markdown(f"### [Download PDF](./{pdf_path})")

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

    if st.button("Clear Temporary Files"):
        if input_path.exists():
            input_path.unlink()
        st.success("Temporary files cleared.")
