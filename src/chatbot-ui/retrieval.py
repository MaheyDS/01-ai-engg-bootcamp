from qdrant_client import QdrantClient
import openai
from core.config import config

qdrant_client = QdrantClient(
    url=f"http://{config.qdrant_url}:6333"
)

def get_embeddings(text, model_name=config.embedding_model):
    response = openai.embeddings.create(
        input=text,
        model=model_name
    )
    return response.data[0].embedding

def retrieve_context(query, top_k=5):
    query_embeddings = get_embeddings(query)
    results = qdrant_client.query_points(
        collection_name=config.qdrant_collection_name,
        query=query_embeddings,
        limit=top_k
    )
    return results

def process_context(context):
    formatted_context = ""

    for chunk in context:
        formatted_context += f"-{chunk}\n"
    
    return formatted_context

def build_prompt(context, question):

    processed_context = process_context(context)

    prompt = f"""
    You are a shopping assistant that can answer questions about the products in-stock.

    You will be given a question and list of context.

    Instructions:
    - You need to answer the question on the provided context only.
    - Never use the word "context" and refer to it as available products.

    Context:
    {processed_context}

    Question:
    {question}

    Answer:
    """

    return prompt

def generate_answer(prompt):
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

def rag_pipeline(question, top_k=5):
    retrieved_context = retrieve_context(question, top_k)
    prompt = build_prompt(retrieved_context, question)
    answer = generate_answer(prompt)
    return answer