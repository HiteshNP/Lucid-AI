import vertexai
import google.generativeai as genai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Image,
    Part,
)
import markdown
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

VERTEX_AI_API_KEY = os.getenv('VERTEX_AI_API_KEY')

genai.configure(api_key=VERTEX_AI_API_KEY)

def text_to_notes(transcript):
    multimodal_model = genai.GenerativeModel("gemini-1.0-pro")
    response = multimodal_model.generate_content(
        [transcript, "Format this professionally in markdown, with headings, bolded keywords, and bullet points"]
    )
    html_text = markdown.markdown(response.text)
    return html_text

def clean_up_text(transcript):
    multimodal_model = genai.GenerativeModel("gemini-1.0-pro")
    response = multimodal_model.generate_content(
        [transcript, "Transform this text so it is grammatically correct, without stutters and repeated words"]
    )
    return response.text

def translate(transcript, language):
    multimodal_model = genai.GenerativeModel("gemini-1.0-pro")
    transcript = clean_up_text(transcript)
    prompt = f"Translate this passage to {language}"
    response = multimodal_model.generate_content([transcript, prompt])
    
    return response.text

def find_keywords(transcript):
    transcript = clean_up_text(transcript)
    
    multimodal_model = genai.GenerativeModel("gemini-1.0-pro")
    response = multimodal_model.generate_content(
        [transcript, "What are the top 5 important keywords of the text? Give it a header \"Top keywords\" and format them as \"1. **Word:** description\""])
    

    try: 
        keywords_only = []
        keywords_only.append(response.text.split("1. **",1)[1].split(":**",1)[0])
        keywords_only.append(response.text.split("2. **",1)[1].split(":**",1)[0])
        keywords_only.append(response.text.split("3. **",1)[1].split(":**",1)[0])
        keywords_only.append(response.text.split("4. **",1)[1].split(":**",1)[0])
        keywords_only.append(response.text.split("5. **",1)[1].split(":**",1)[0])

        descriptions_only = []
        shortened = response.text.split(":**",1)[1]
        descriptions_only.append(shortened.split(":** ",1)[1].split("\n2.",1)[0])
        shortened = shortened.split(":** ",1)[1]
        descriptions_only.append(shortened.split(":** ",1)[1].split("\n3.",1)[0])
        shortened = shortened.split(":** ",1)[1]
        descriptions_only.append(shortened.split(":** ",1)[1].split("\n4.",1)[0])
        shortened = shortened.split(":** ",1)[1]
        descriptions_only.append(shortened.split(":** ",1)[1].split("\n5.",1)[0])
        shortened = shortened.split(":** ",1)[1]
        descriptions_only.append(shortened.split(":** ",1)[1])
    except:
        keywords_only = [0, 0, 0, 0, 0]
        descriptions_only = [0, 0, 0, 0, 0]
    
    return response.text, keywords_only, descriptions_only

    
if __name__ == "__main__":
    
    project_id = "genaigensis2024"
    # Initialize Vertex AI
    vertexai.init(project=project_id, location="us-central1")
    transcript = open("transcript.txt", "r")
    file = transcript.read()
    
    cleaned_text = clean_up_text(file)
    
    flashcards, keywords_only, descriptions_only = find_keywords(cleaned_text)
    
    print("\n")
    print("\n")
    print(flashcards)
    
    print("\n")
    print("\n")
    print(keywords_only)

    print("\n")
    print("\n")
    print(descriptions_only)