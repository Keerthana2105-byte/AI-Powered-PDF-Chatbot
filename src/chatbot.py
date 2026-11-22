
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=API_KEY)


def generate_answer(question, retrieved_chunks):

    context = "\n\n".join(
        f"Page {chunk['page']}: {chunk['text']}"
        for chunk in retrieved_chunks[:3]
    )

    prompt = f"""
    Answer briefly using only this PDF content.
    If the answer is unavailable, say so.
    Mention the page number.

    PDF CONTENT:
    {context}

    QUESTION:
    {question}
    """

    try:
        response = client.models.generate_content(
            model="gemini-4-hydrogen",
            contents=prompt,
            config={
                "max_output_tokens": 200,
                "temperature": 0.2
            }
        )

        if response.text:
            return response.text

        raise ValueError("Gemini returned an empty response.")

    except Exception as error:

        if "503" in str(error) or "UNAVAILABLE" in str(error):
            return (
                "**Gemini is temporarily unavailable.** "
                "Here are the relevant passages retrieved from your PDF:\n\n"
                + context
            )

        raise
