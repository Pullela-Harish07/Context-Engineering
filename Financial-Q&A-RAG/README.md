# Financial Q&A RAG System for SEC 10-Q Filings

An advanced Retrieval-Augmented Generation (RAG) system specifically designed to extract and answer questions from Amazon's SEC Form 10-Q financial documents. This system combines intelligent document parsing, vector search, and Google's Gemini AI to provide accurate, context-aware answers to financial queries.

## 🎯 Use Case

**Problem**: SEC 10-Q forms are dense, complex financial documents spanning hundreds of pages with intricate tables, legal jargon, and interconnected financial data. Finding specific information manually is time-consuming and error-prone.

**Solution**: This RAG system automatically:
- Extracts and structures content from PDF 10-Q filings
- Preserves critical financial tables and their formatting
- Enables natural language queries about financial metrics
- Provides accurate, sourced answers with relevant context
- Supports complex financial analysis queries

**Target Users**:
- Financial Analysts researching company performance
- Investors making data-driven decisions
- Researchers studying financial trends
- Accountants verifying financial statements
- Students learning financial analysis

## ✨ Key Features

- **Intelligent PDF Processing**: Uses Docling to extract structured content while preserving financial table integrity
- **Table-Aware Chunking**: Custom splitting logic that keeps financial tables intact for accurate retrieval
- **Hybrid Retrieval System**: Combines semantic vector search with keyword matching for financial terms
- **Specialized Financial Prompts**: Expert-level prompt engineering for accurate financial data extraction
- **Interactive UI**: Clean Streamlit interface for easy document upload and querying
- **Context Transparency**: View retrieved document chunks to verify answer sources
- **Sample Questions**: Pre-built queries to help users get started quickly

## 🏗️ System Architecture

```
PDF Upload → Docling Extraction → Markdown Conversion → Smart Chunking
    ↓
Vector Store (FAISS) + Embedding (HuggingFace)
    ↓
Hybrid Retrieval (Semantic + Keyword)
    ↓
Context Formation → Gemini AI → Structured Answer
```

## 📚 Libraries & Technologies

### Core Framework
- **Streamlit** (`streamlit`): Web application framework for the user interface
- **LangChain** (`langchain`, `langchain-community`): Orchestration framework for RAG pipeline

### Document Processing
- **Docling** (`docling`): Advanced PDF extraction with structure preservation
- **LangChain Text Splitters**: Intelligent document chunking with overlap

### Vector Store & Embeddings
- **FAISS** (`faiss-cpu`): Efficient similarity search and clustering of dense vectors
- **HuggingFace Embeddings** (`langchain-huggingface`): Sentence transformer embeddings
  - Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional embeddings)

### AI Model
- **Google Gemini 2.5 Flash** (`langchain-google-genai`): Large language model for answer generation
  - Temperature: 0.0 (deterministic, factual responses)
  - Max tokens: 2500

### Utilities
- **Python-dotenv** (`python-dotenv`): Environment variable management

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- 2GB+ RAM (for embedding model and FAISS index)

### Step 1: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install streamlit langchain langchain-community langchain-google-genai \
    langchain-huggingface docling faiss-cpu python-dotenv
```

Or using a requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

## 📖 Usage

### Running the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the System

1. **Upload PDF**: Click "Upload PDF" and select an SEC 10-Q form (PDF format)
2. **Wait for Processing**: The system will extract, chunk, and index the document
3. **Ask Questions**: Enter natural language questions about the financial data
4. **Review Answers**: Get detailed answers with source context
5. **Verify Sources**: Expand "Retrieved Context" to see the exact document chunks used

### Sample Questions

**Financial Performance:**
- What was Amazon's total revenue in Q3 2024?
- What was the net income for Q3 2024?
- What were the earnings per share (EPS) in Q3 2024?
- How did revenue compare between Q3 2024 and Q3 2023?

**Segment Analysis:**
- What was the revenue for AWS in Q3 2024?
- How did the North America segment perform?
- Compare operating income across all segments

**Cash Flow:**
- What were Amazon's capital expenditures in Q3 2024?
- What was the free cash flow?

**Balance Sheet:**
- What is Amazon's total long-term debt as of September 30, 2024?
- What were the total assets?

## 🔧 How It Works

### 1. Document Ingestion (`ingest.py`)

**PDF Extraction:**
```python
extract_pdf_content() → Uses Docling to convert PDF to structured Markdown
```
- Preserves tables, headers, and document structure
- Extracts text with high accuracy
- Converts to markdown for easier processing

**Smart Chunking:**
```python
get_markdown_splits() → Splits by major sections (# and ##)
recursive_refine() → Further splits large chunks while preserving tables
```
- Detects financial tables (presence of `|` and numbers)
- Keeps tables under 5000 characters intact
- Splits larger non-table content with overlap for context continuity
- Chunk size: 2500 characters, Overlap: 400 characters

### 2. Vector Store Setup (`vectorstore.py`)

**Embedding & Indexing:**
```python
setup_vector_store() → Creates FAISS index with HuggingFace embeddings
```
- Embeds each chunk into 384-dimensional vectors
- Uses FAISS L2 (Euclidean distance) index for fast similarity search
- Stores in-memory for rapid retrieval

**Hybrid Retrieval:**
```python
hybrid_retrieve() → Combines semantic search + keyword matching
```
- **Semantic Search**: Uses MMR (Maximal Marginal Relevance) to retrieve diverse, relevant chunks
- **Keyword Boosting**: Prioritizes chunks containing financial terms (revenue, net income, EPS, etc.)
- **Table Prioritization**: Gives higher weight to chunks with financial tables
- Retrieves top 15 unique documents

### 3. RAG Pipeline (`rag_pipeline.py`)

**Query Processing:**
```python
run_rag() → Orchestrates retrieval and answer generation
```
1. Retrieves relevant documents using hybrid approach
2. Formats context with clear document separation
3. Prioritizes table-containing documents first
4. Sends formatted context + question to Gemini AI
5. Returns structured answer with source documents

### 4. Prompt Engineering (`prompts.py`)

**Specialized Financial Prompt:**
- **Terminology Guide**: Explains financial terms and their equivalents
- **Hierarchy Understanding**: Teaches model about financial statement structure
- **Answer Format**: Enforces structured, accurate responses
- **Quality Checks**: Built-in validation before responding
- **Comparison Logic**: Instructions for year-over-year analysis

### 5. User Interface (`app.py`)

**Session State Management:**
- Caches processed PDF to avoid reprocessing
- Maintains retriever and chunks in memory
- Ensures fast subsequent queries

**Interactive Features:**
- File upload widget
- Progress indicators
- Sample questions expander
- Context viewer for transparency