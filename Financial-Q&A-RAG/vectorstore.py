import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings


def setup_vector_store(chunks):
    """
    Setup vector store with financial-optimized embeddings
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    dim = len(embeddings.embed_query("test"))
    index = faiss.IndexFlatL2(dim)

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

    vector_store.add_documents(chunks)
    return vector_store


def get_retriever(vector_store):
    """
    Enhanced retriever optimized for financial documents with tables
    """
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 15,
        }
    )


def hybrid_retrieve(query, vector_store, all_chunks):
    """
    Hybrid retrieval: semantic search + keyword matching for financial terms
    """
    # Get semantic results
    retriever = get_retriever(vector_store)
    semantic_docs = retriever.get_relevant_documents(query)


    financial_keywords = [
        'revenue', 'net sales', 'total net sales', 'operating income',
        'net income', 'earnings per share', 'EPS', 'consolidated statements',
        'balance sheet', 'cash flow', 'long-term debt', 'stockholders equity',
        'total assets', 'total liabilities', 'AWS', 'segment', 'nine months ended'
    ]

    # Keyword boost: find chunks with financial statement titles
    keyword_docs = []
    query_lower = query.lower()

    for doc in all_chunks:
        content_lower = doc.page_content.lower()


        if any(keyword in content_lower for keyword in financial_keywords):

            if '|' in doc.page_content and any(char.isdigit() for char in doc.page_content):
                keyword_docs.append(doc)


    all_docs = semantic_docs + keyword_docs[:5]


    seen = set()
    unique_docs = []
    for doc in all_docs:
        doc_id = doc.page_content[:100]
        if doc_id not in seen:
            seen.add(doc_id)
            unique_docs.append(doc)

    return unique_docs[:15]