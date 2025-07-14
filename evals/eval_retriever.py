import os

# Now we can import normally using the symbolic link
from chatbot_ui.core.config import config
from chatbot_ui.retrieval import rag_pipeline

from langsmith import Client
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

ls_client = Client(api_key=os.environ["LANGSMITH_API_KEY"])
qdrant_client = QdrantClient(
    url=f"http://{config.qdrant_url}:6333"
)

from ragas.dataset_schema import SingleTurnSample 
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithoutReference, LLMContextRecall, NonLLMContextRecall

ragas_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1"))
ragas_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

import asyncio

def ragas_faithfullness(run, example):
    async def _eval():
        sample = SingleTurnSample(
                user_input=run.inputs.get("question", ""),
                response=run.outputs.get("answer", ""),
                retrieved_contexts=run.outputs.get("retrieved_context", [])
            )
        scorer = Faithfulness(llm=ragas_llm)
        score = await scorer.single_turn_ascore(sample)
        return {"key": "faithfulness", "score": score}
    return asyncio.run(_eval())

def ragas_respone_relevancy(run, example):
    async def _eval():
        sample = SingleTurnSample(
                user_input=run.inputs.get("question", ""),
                response=run.outputs.get("answer", ""),
                retrieved_contexts=run.outputs.get("retrieved_context", [])
            )
        scorer = ResponseRelevancy(llm=ragas_llm, embeddings=ragas_embeddings)
        score = await scorer.single_turn_ascore(sample)
        return {"key": "response_relevancy", "score": score}
    return asyncio.run(_eval())

def ragas_context_precision(run, example):
    async def _eval():
        sample = SingleTurnSample(
                user_input=run.inputs.get("question", ""),
                response=run.outputs.get("answer", ""),
                retrieved_contexts=run.outputs.get("retrieved_context", [])
            )
        scorer = LLMContextPrecisionWithoutReference(llm=ragas_llm)
        score = await scorer.single_turn_ascore(sample)
        return {"key": "context_precision", "score": score}
    return asyncio.run(_eval())

def ragas_context_recall_llm_based(run, example):
    async def _eval():
        sample = SingleTurnSample(
                user_input=run.inputs.get("question", ""),
                response=run.outputs.get("answer", ""),
                reference=example.outputs.get("ground_truth", ""),
                retrieved_contexts=run.outputs.get("retrieved_context", [])
            )
        scorer = LLMContextRecall(llm=ragas_llm)
        score = await scorer.single_turn_ascore(sample)
        return {"key": "context_recall_llm", "score": score}
    return asyncio.run(_eval())

def ragas_context_recall_non_llm(run, example):
    async def _eval():
        # Check what keys are available and use the appropriate ones
        retrieved_contexts = run.outputs.get("retrieved_context", [])
        reference_contexts = example.outputs.get("contexts", example.outputs.get("retrieved_context", []))
        
        # Skip if either context is empty to avoid max() error
        if not retrieved_contexts or not reference_contexts:
            return {"key": "context_recall_non_llm", "score": 0.0}
        
        sample = SingleTurnSample(
                retrieved_contexts=retrieved_contexts,
                reference_contexts=reference_contexts
            )
        scorer = NonLLMContextRecall()
        score = await scorer.single_turn_ascore(sample)
        return {"key": "context_recall_non_llm", "score": score}
    return asyncio.run(_eval())

results = ls_client.evaluate(
    lambda x: rag_pipeline(x["question"], qdrant_client),
    data="rag-evaluation-dataset",
    evaluators=[
        ragas_faithfullness,
        ragas_respone_relevancy,  
        ragas_context_precision,
        ragas_context_recall_llm_based,
        ragas_context_recall_non_llm
    ],
    experiment_prefix="rag-evalualtion-dataset"
)