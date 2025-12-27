import streamlit as st
from ingest import extract_pdf_content, get_markdown_splits, recursive_refine
from vectorstore import setup_vector_store, get_retriever
from rag_pipeline import run_rag

st.set_page_config("RAG", layout="wide")

st.title("Financial Q&A (Amazon)")

# Initialize session state
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'all_chunks' not in st.session_state:
    st.session_state.all_chunks = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

pdf = st.file_uploader("Upload PDF", type="pdf")

# Process PDF only when a new file is uploaded
if pdf and not st.session_state.pdf_processed:
    with st.spinner("Processing PDF..."):
        # Save uploaded file
        with open("temp.pdf", "wb") as f:
            f.write(pdf.read())

        # Extract and process
        markdown = extract_pdf_content("temp.pdf")
        header_chunks = get_markdown_splits(markdown)
        refined_chunks = recursive_refine(header_chunks)

        # Store chunks for hybrid retrieval
        st.session_state.all_chunks = refined_chunks

        # Setup vector store and retriever
        vector_store = setup_vector_store(refined_chunks)
        st.session_state.retriever = get_retriever(vector_store)
        st.session_state.pdf_processed = True

    st.success("PDF processed successfully! You can now ask questions.")
    st.info(f"Processed {len(refined_chunks)} document chunks")

# Question input - only show if PDF is processed
if st.session_state.pdf_processed:
    st.markdown("---")

    # Sample questions in expander
    with st.expander("Sample Questions"):
        st.markdown("""
        **Financial Performance:**
        - What was Amazon's total revenue in Q3 2024?
        - What was the net income for Q3 2024?
        - What were the earnings per share in Q3 2024?

        **Segment Analysis:**
        - What was the revenue for AWS in Q3 2024?
        - How did North America and International segments perform?

        **Cash Flow:**
        - What were Amazon's capital expenditures in Q3 2024?

        **Balance Sheet:**
        - What is Amazon's total long-term debt as of September 30, 2024?
        """)

    question = st.text_input("Ask a question about the SEC 10-Q",
                             placeholder="e.g., What was the total revenue in Q3 2024?")

    if question:
        with st.spinner("Searching for answer..."):
            answer, docs = run_rag(
                question,
                st.session_state.retriever,
                st.session_state.all_chunks
            )

        st.markdown("### Answer")
        st.markdown(answer)

        with st.expander("Retrieved Context"):
            for i, d in enumerate(docs, 1):
                st.markdown(f"**Chunk {i}**")
                st.text(d.page_content[:2000])
                st.markdown("---")