# Slides2Tutorials

Slides2Tutorials is a co-creative system designed to transform lecture slides (PDFs) into engaging audio and visual tutorials. The system generates an explanatory audio narrative, a video tutorial, and a detailed PDF combining the slides and the generated speech. The goal is to make learning more accessible and personalized by enabling users to customize the knowledge level, voice preferences, humor, and detail level of the generated content.

## Features

- **Lecture Slide to Tutorial Conversion**: Converts lecture slides (PDF) into:
  - Audio tutorial
  - PDF with explanatory text
  - Optionally, a video (future updates)
  
- **Customization Options**:
  - Knowledge Level: Beginner, Medium, Advanced, or Expert
  - Voice Gender: Male or Female
  - Humor: Add humor to the narrative or keep it formal
  - Detail Level: Adjust tutorial length and depth

- **Advanced Natural Language Processing**:
  - Summarizes and cleans slide content
  - Generates engaging and concise narratives using pre-trained language models
  - Text-to-Speech (TTS) to produce high-quality audio tutorials

- **Output**:
  - An audio file (.mp3)
  - A polished PDF combining slides and generated explanations

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LI-SUJU/slides2tutorials.git
   cd slides2tutorials
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Install additional system packages for gTTS, reportlab, and PyPDF2 if needed:
   ```bash
   sudo apt-get install python3-tk

## Usage
### Running the Streamlit App
1. Start the App:
   ```bash
   streamlit run app.py
2. Open the provided link in your browser (default: http://localhost:8501).
3. Upload your lecture slides (PDF) and customize the settings using the sidebar options:
  - Select Knowledge Level, Voice Gender, Humor, and Detail Level.
  - Click Generate Audio Tutorial and PDF.
4.Download the generated tutorial files:
  - Audio Tutorial (.mp3)
  - Explanatory PDF (.pdf)
### Command line mode(optional):
   ```bash
   python cc_fin_v1_0.py --input <input-pdf> --output-audio <output-audio> --output-pdf <output-pdf>
```
### Run it on Colab with a .ipynb implementation:
https://github.com/LI-SUJU/slides2tutorials/blob/main/CC_fin_v1.0.ipynb


