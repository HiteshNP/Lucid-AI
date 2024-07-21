# Lucid-AI: Revolutionizing Education with AI

## Overview

Lucid-AI is a transformative web application that leverages advanced AI technologies to make learning more accessible, engaging, and effective for all students. It integrates tools like Generative AI, Multi-Modal Learning, and Retrieval-Augmented Generation (RAG) to adapt educational resources to diverse learning styles and needs, thereby supporting inclusive and equitable quality education.

## Table of Contents

1. [Domain of AI in Education](#the-domain-of-ai-in-education)
2. [Problem Statement](#problem-statement)
3. [Technologies Addressing Educational Challenges](#technologies-addressing-educational-challenges)
4. [Outcome](#outcome)
5. [Features](#features)
    - [LucidAI Audio Decoder](#listen-read-learn-audio-decoder)
    - [Multilingual Translation](#clear-understanding-multilingual-translation)
    - [Accented Speech Translation](#hear-it-your-way-effortless-understanding)
    - [Interactive Flashcards](#flash-your-way-to-the-top-interactive-learning-made-fun)
    - [Boring Slide Eradicator](#lucidai-boring-slide-eradicator)
    - [Chat with Multiple PDFs](#chat-with-multiple-pdfs)
    - [Summary-Sorcerer](#from-confusion-to-clarity-the-lucidai-summary-sorcerer)
6. [Accomplishments](#accomplishments)
7. [Challenges](#challenges)
8. [What We Learned](#what-we-learned)
9. [Future Works](#future-works)
10. [Project Architecture](#project-architecture)
11. [Running the Project](#running-the-project)

## The Domain of AI in Education

Artificial Intelligence (AI) is revolutionizing education by enabling personalized learning, automating administrative tasks, and enhancing teaching and learning processes. AI's ability to process vast amounts of data and adapt to individual learner needs aligns with Sustainable Development Goal 4 (SDG 4), ensuring inclusive and equitable quality education.

## Problem Statement

Despite progress in access to education, quality and inclusivity remain major challenges. Traditional educational resources often fail to cater to diverse learning styles and special needs, creating barriers for many students. Innovative solutions are required to address these challenges effectively.

## Technologies Addressing Educational Challenges

Advanced AI technologies such as Generative AI, Multi-Modal Learning, and Retrieval-Augmented Generation (RAG) are at the forefront of addressing educational challenges. These technologies enable the creation of adaptable learning resources, support diverse learning styles, and enhance the accessibility and quality of educational content.

## Outcome

Applying advanced AI solutions in education aims to reduce inequalities, enhance learning experiences, and support lifelong learning opportunities for all. By leveraging technologies like Generative AI and Multi-Modal Learning, educational tools like LucidAI can be developed to cater to individual learning needs, improve the quality of educational materials, and make learning more engaging and effective.

## Features

### 🎧 Listen, Read, Learn: Audio Decoder

- 🎙 Instantly transcribe MP3 files into readable text
- 📄 Upload txt files for an enhanced learning experience
- 🧠 Boost comprehension and retention
- 📝 Take notes and organize thoughts
- 📈 Review and track progress

### Clear Understanding: Multilingual Translation

- Translate transcribed text from audio into various languages including 🇬🇧 English, 🇮🇳 Kannada, 🇮🇳 Hindi, 🇮🇳 Tamil, 🇮🇳 Telugu, 🇮🇳 Malayalam, 🇫🇷 French, 🇪🇸 Spanish, 🇰🇷 Korean, 🇦🇪 Arabic, and many more!
- Read and understand audio content in your native language

### 🎵 Hear It Your Way: Effortless Understanding

- 🎚 Adjust accents in audio files to your preference
- 🔊 Enhance audio clarity and comprehension
- 🚀 Boost learning and productivity

### 🚀 Flash Your Way to the Top: Interactive Learning Made Fun

- 💡 Create digital flashcards with a click
- 📚 Study modes for every learning style
- 🎯 Track progress and stay motivated

### ✨ LucidAI Boring-Slide-Eradicator

- 🎨 Transform confusing lecture slides into engaging material
- 🧙‍♂ Generate clearer slides using Google Gemini
- 📜 Specify citations, exclude unnecessary slides, and choose PPT themes

### 📚 Chat with Multiple PDFs

- 📁 Upload multiple PDF documents
- 🤖 Interact with content via a chatbot interface
- 🔍 Extract information, ask questions, and get summaries
- 🗂 Enhance learning and research efficiency by consolidating information

### 🔮 From Confusion to Clarity: The LucidAI-Summary-Sorcerer

- 📚 Summarizes lengthy texts into concise, clear summaries
- ⚡ Extracts key points swiftly and accurately
- 💡 Highlights core concepts for better understanding

## Project Architecture

The project architecture consists of a front-end built with HTML, CSS, and Bootstrap, and a back-end built with Python (Flask), Gemini API, AssemblyAI, and Eleven Labs API. Here is a high-level overview of the architecture:

![arch1](/static/arch1.png)

![Uarch2](/static/architecture_pptgen.png)

## Running the Project

### Prerequisites

- Python 3.x
- Flask
- Streamlit
- Required API keys (Gemini, AssemblyAI, Eleven Labs)

### Installation

1. *Clone the repository*

    ```bash
    git clone https://github.com/your-repo/lucid-ai.git
    cd lucid-ai
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables: Create a `.env` file in the project root and add your API keys:**

    ```bash
    GEMINI_API_KEY=your_gemini_api_key
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
    ```
4. **Start the Flask server**

    ```bash
    python app.py
    ```

### Accessing the Application

Open your web browser and navigate to http://localhost:5000 to access Lucid-AI.

Thank you for exploring Lucid-AI! We hope this tool enhances your learning experience and supports your educational journey. If you have any questions or feedback, please feel free to reach out.

