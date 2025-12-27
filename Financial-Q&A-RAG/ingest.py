from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document


def extract_pdf_content(file_path: str) -> str:
    """
    Extract structured PDF content using Docling.
    Returns markdown text.
    """
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()


def get_markdown_splits(markdown_content: str):
    """
    Split markdown while preserving financial tables
    """
    # Split by major sections first
    sections = []
    current_section = []

    lines = markdown_content.split('\n')

    for line in lines:
        current_section.append(line)

        # Create chunks at major headers or after substantial content
        if line.startswith('# ') or line.startswith('## '):
            if len('\n'.join(current_section)) > 500:
                sections.append('\n'.join(current_section))
                current_section = []


    if current_section:
        sections.append('\n'.join(current_section))

    # Convert to Document objects
    documents = [Document(page_content=section) for section in sections if section.strip()]

    return documents


def recursive_refine(chunks, chunk_size=2500, overlap=400):
    """
    Refine chunks while keeping tables intact
    Only split if chunk is too large AND doesn't contain critical tables
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n\n",  # Multiple newlines
            "\n\n",  # Paragraph breaks
            "\n",  # Line breaks
            ". ",  # Sentences
            ", ",  # Clauses
            " ",  # Words
        ]
    )

    refined = []

    for doc in chunks:
        content = doc.page_content

        # Check if this chunk contains financial tables (has characters and numbers)
        has_table = '|' in content and any(char.isdigit() for char in content)

        # If it has a table and is under 5000 chars, keep it whole
        if has_table and len(content) < 5000:
            refined.append(doc)
        else:
            # Otherwise split normally
            refined.extend(splitter.split_documents([doc]))

    return refined