import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import get_sec_10q_prompt

load_dotenv()


def format_docs(docs):
    """
    Format documents with clear separation and numbering
    Prioritize documents with tables
    """

    table_docs = [d for d in docs if '|' in d.page_content]
    text_docs = [d for d in docs if '|' not in d.page_content]

    sorted_docs = table_docs + text_docs

    formatted_parts = []
    for i, doc in enumerate(sorted_docs, 1):
        formatted_parts.append(f"--- Document {i} ---\n{doc.page_content}\n")

    return "\n".join(formatted_parts)


def run_rag(query, retriever, all_chunks=None):
    """
    Run RAG pipeline with hybrid retrieval if chunks available
    """
    # If all_chunks provided, use hybrid retrieval
    if all_chunks:
        from vectorstore import hybrid_retrieve
        docs = hybrid_retrieve(query, retriever.vectorstore, all_chunks)
    else:
        # Fallback to standard retrieval
        docs = retriever.get_relevant_documents(query)

    context = format_docs(docs)

    prompt = get_sec_10q_prompt()

    # Use Gemini with optimized parameters
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        max_output_tokens=2500,
        google_api_key=os.environ["GOOGLE_API_KEY"],
    )

    chain = prompt | llm

    answer = chain.invoke(
        {"question": query, "context": context}
    ).content

    return answer, docs