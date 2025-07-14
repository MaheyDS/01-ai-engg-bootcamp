import openai
from chatbot_ui.core.config import config
from langsmith import traceable, get_current_run_tree



@traceable(
    name="embed_query",
    run_type="embedding",
    metadata={"ls_provider": config.embedding_model_provider, "ls_model_name": config.embedding_model},
)
def get_embeddings(text, model_name=config.embedding_model):
    response = openai.embeddings.create(
        input=text,
        model=model_name
    )
    current_run = get_current_run_tree()
    if current_run:
        current_run.metadata["usage_metadata"] = {
            "input_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens
        }

    return response.data[0].embedding

@traceable(
    name="retrieve_topn",
    run_type="retriever",
)
def retrieve_context(query, qdrant_client, top_k=5):
    query_embeddings = get_embeddings(query)
    results = qdrant_client.query_points(
        collection_name=config.qdrant_collection_name,
        query=query_embeddings,
        limit=top_k
    )

    retrieved_context_ids =[]
    retrieved_context = []
    similarity_score = []

    for result in results.points:
        retrieved_context_ids.append(result.id)
        # Safely handle missing or None payloads
        text = None
        if result.payload and isinstance(result.payload, dict):
            text = result.payload.get('text')
        retrieved_context.append(text)
        similarity_score.append(result.score)

    return {
        "retrieved_context_ids": retrieved_context_ids,
        "retrieved_context": retrieved_context,
        "similarity_score": similarity_score
    }

@traceable(
    name="format_retrieved_context",
    run_type="prompt",
)
def process_context(context):
    formatted_context = ""

    for chunk in context["retrieved_context"]:
        formatted_context += f"-{chunk}\n"
    
    return formatted_context

@traceable(
    name="render_prompt",
    run_type="prompt",
)
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

@traceable(
    name="generate_answer",
    run_type="llm",
    metadata={"ls_provider": config.generation_model_provider, "ls_model_name": config.generation_model},
)
def generate_answer(prompt):
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    current_run = get_current_run_tree()
    if current_run and response.usage is not None:
        current_run.metadata["usage_metadata"] = {
            "input_tokens": getattr(response.usage, "prompt_tokens", None),
            "output_tokens": getattr(response.usage, "completion_tokens", None),
            "total_tokens": getattr(response.usage, "total_tokens", None)
        }

    return response.choices[0].message.content

@traceable(
    name="rag_pipeline"
)
def rag_pipeline(question, qdrant_client, top_k=5):

    retrieved_context = retrieve_context(question, qdrant_client, top_k)
    prompt = build_prompt(retrieved_context, question)
    answer = generate_answer(prompt)
    final_result = {
        "answer": answer,
        "question": question,
        "retrieved_context_ids": retrieved_context["retrieved_context_ids"],
        "retrieved_context": retrieved_context["retrieved_context"],
        "similarity_score": retrieved_context["similarity_score"]
    }


    return final_result