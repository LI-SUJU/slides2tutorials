import re
from transformers import pipeline
from PyPDF2 import PdfReader
from gtts import gTTS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Function to clean text and remove unwanted phrases
def clean_text(text, unwanted_phrases=None):
    if unwanted_phrases is None:
        unwanted_phrases = [
            "Leiden University",
            "Discover the world",
            "Discover the world at Leiden University",
        ]
    for phrase in unwanted_phrases:
        text = re.sub(rf'\b{re.escape(phrase)}\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Function to remove repeated phrases or sentences
def remove_repetitions(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    seen = set()
    cleaned_sentences = []
    for sentence in sentences:
        normalized_sentence = sentence.strip().lower()
        if normalized_sentence not in seen:
            seen.add(normalized_sentence)
            cleaned_sentences.append(sentence.strip())
    return ' '.join(cleaned_sentences)


# Function to summarize text
def summarize_text(text, model_name="facebook/bart-large-cnn"):
    summarizer = pipeline("summarization", model=model_name, device=0)
    try:
        if not text.strip():
            return "This slide contains no text or mostly images. Please refer to the visuals."
        summary = summarizer(
            text,
            max_length=120,
            min_length=30,
            repetition_penalty=2.5,
            do_sample=False
        )
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text


# Function to generate a narrative with user preferences
def generate_narrative(summary, voice_gender, humor, detail_level, model_name="google/flan-t5-base"):
    generator = pipeline("text2text-generation", model=model_name, device=0)
    try:
        if "no text" in summary.lower():
            return summary

        # Construct the narrative prompt based on user preferences
        humor_text = "Include some humor." if humor else "Do not include humor."
        detail_text = (
            "Provide a detailed explanation." if detail_level > 5 else "Provide a concise explanation."
        )
        prompt = (
            f"Explain the following content in a {voice_gender.lower()} voice. "
            f"{humor_text} {detail_text} Ensure clarity and engagement.\n\n"
            f"{summary}"
        )
        result = generator(
            prompt,
            max_length=300,
            repetition_penalty=2.5,
            temperature=0.7,
            do_sample=True
        )
        return remove_repetitions(result[0]["generated_text"])
    except Exception as e:
        print(f"Error generating narrative: {e}")
        return summary


# Function to create a combined voice-over file using Google TTS
def generate_combined_voice_over(narratives, output_path="combined_voiceover.mp3"):
    try:
        combined_text = "\n\n".join(narratives)
        tts = gTTS(text=combined_text, lang='en')
        tts.save(output_path)
        print(f"Combined voice-over saved to {output_path}")
    except Exception as e:
        print(f"Error generating voice-over: {e}")


# Function to generate a PDF from narratives
def generate_formatted_pdf(narratives, output_file="Generated_Narratives.pdf"):
    try:
        c = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter
        margin = 50
        text_width = width - 2 * margin
        y_position = height - margin  # Start near the top

        # Title Page
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, y_position, "Generated Narratives")
        y_position -= 50  # Adjust position for the next content

        for narrative in narratives:
            page_title, page_content = narrative.split(":", 1)
            if y_position < margin:  # If text overflows, create a new page
                c.showPage()
                y_position = height - margin

            # Draw title
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, page_title.strip())
            y_position -= 20

            # Split text into lines manually to fit within the margins
            c.setFont("Helvetica", 12)
            words = page_content.strip().split()
            line = ""
            for word in words:
                if c.stringWidth(line + word + " ", "Helvetica", 12) < text_width:
                    line += word + " "
                else:
                    c.drawString(margin, y_position, line.strip())
                    y_position -= 15  # Adjust line spacing
                    line = word + " "
                    if y_position < margin:  # If text overflows, create a new page
                        c.showPage()
                        y_position = height - margin
            # Draw the last line
            if line.strip():
                c.drawString(margin, y_position, line.strip())
                y_position -= 15

        # Save the PDF
        c.save()
        print(f"Formatted PDF saved to '{output_file}'")
    except Exception as e:
        print(f"Error generating formatted PDF: {e}")


# Function to process the entire pipeline
def process_slides(file_path, voice_gender, humor, detail_level):
    try:
        pages = PdfReader(file_path).pages
        narratives = []
        for i, page in enumerate(pages, start=1):
            raw_text = page.extract_text()
            clean_page_text = clean_text(raw_text)
            deduplicated_text = remove_repetitions(clean_page_text)
            summary = summarize_text(deduplicated_text)
            narrative = generate_narrative(summary, voice_gender, humor, detail_level)
            narratives.append(f"Page {i}:\n{narrative}")

        # Generate outputs
        audio_path = "output_audio_tutorial.mp3"
        pdf_path = "output_tutorial.pdf"
        generate_combined_voice_over(narratives, output_path=audio_path)
        generate_formatted_pdf(narratives, output_file=pdf_path)

        return audio_path, pdf_path
    except Exception as e:
        print(f"Error processing slides: {e}")
        return None, None
