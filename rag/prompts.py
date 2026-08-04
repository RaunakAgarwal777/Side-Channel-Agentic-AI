"""
prompts.py
Centralized prompt templates for the RAG loop, kept in one file per the
"1 prompt library, not 15" simplification.
"""

QUERY_REWRITE_PROMPT = """You are refining a query for a side-channel attack knowledge base.
Original query: {query}
Prior attempts: {history}

Rewrite the query to be more specific and retrieval-friendly. Return only the rewritten query."""

RELEVANCE_GRADE_PROMPT = """You are grading whether retrieved documents are relevant to a query.
Query: {query}

Documents:
{documents}

Are these documents relevant enough to answer the query? Answer strictly "yes" or "no"."""

HALLUCINATION_GRADE_PROMPT = """You are checking whether an answer is grounded in the given context.
Context:
{context}

Answer:
{answer}

Is the answer fully supported by the context (no fabricated claims)? Answer strictly "yes" or "no"."""

ANSWER_QUALITY_PROMPT = """You are checking whether an answer fully addresses a question.
Question: {query}
Answer: {answer}

Does the answer sufficiently and completely address the question? Answer strictly "yes" or "no"."""

GENERATE_ANSWER_PROMPT = """You are a side-channel security analyst assistant.
Use the context below to answer the question. Cite specific evidence where possible.

Context:
{context}

Question: {query}

Answer:"""
