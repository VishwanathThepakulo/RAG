from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
def calling(query, context):
    model = init_chat_model(
        model='qwen/qwen3-32b',
        model_provider='groq',
        groq_api_key=api_key,
        temperature=0.7,
        timeout=30,
        max_tokens=1000,
        max_retries=6,
    )
    prompt = f"""Answer the question using the context below.
    Context:
    {context}
    Question:
    {query}
    Answer clearly."""
    ai_msg = model.invoke(prompt)
    # print(type(ai_msg))
    # print(ai_msg.content)
    return ai_msg.content
