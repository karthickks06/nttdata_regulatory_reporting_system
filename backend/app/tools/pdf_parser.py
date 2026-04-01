"""PDF parsing tool using PyPDF2 and pdfplumber"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import PyPDF2
import pdfplumber


async def parse_pdf(file_path: str) -> Dict[str, Any]:
    """
    Parse PDF document and extract text, tables, and metadata.

    Args:
        file_path: Path to PDF file

    Returns:
        Dictionary containing extracted content
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        result = {
            "text": "",
            "pages": [],
            "tables": [],
            "images": [],
            "metadata": {}
        }

        # Extract metadata using PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            # Get metadata
            metadata = pdf_reader.metadata
            if metadata:
                result["metadata"] = {
                    "title": metadata.get('/Title', ''),
                    "author": metadata.get('/Author', ''),
                    "subject": metadata.get('/Subject', ''),
                    "creator": metadata.get('/Creator', ''),
                    "producer": metadata.get('/Producer', ''),
                    "creation_date": str(metadata.get('/CreationDate', '')),
                    "modification_date": str(metadata.get('/ModDate', ''))
                }

            result["metadata"]["page_count"] = len(pdf_reader.pages)

        # Extract text and tables using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            all_text = []

            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                page_text = page.extract_text() or ""
                all_text.append(page_text)

                page_data = {
                    "page_number": page_num,
                    "text": page_text,
                    "width": page.width,
                    "height": page.height
                }

                result["pages"].append(page_data)

                # Extract tables
                tables = page.extract_tables()
                if tables:
                    for table_idx, table in enumerate(tables):
                        result["tables"].append({
                            "page": page_num,
                            "table_index": table_idx,
                            "data": table
                        })

            result["text"] = "\n".join(all_text)

        result["success"] = True
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }


async def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract plain text from PDF.

    Args:
        file_path: Path to PDF file

    Returns:
        Extracted text
    """
    result = await parse_pdf(file_path)
    if result.get("success"):
        return result.get("text", "")
    return ""


async def extract_tables_from_pdf(file_path: str) -> List[List[List[str]]]:
    """
    Extract tables from PDF.

    Args:
        file_path: Path to PDF file

    Returns:
        List of tables (each table is a list of rows)
    """
    result = await parse_pdf(file_path)
    if result.get("success"):
        return [table["data"] for table in result.get("tables", [])]
    return []


async def get_pdf_page_count(file_path: str) -> int:
    """
    Get number of pages in PDF.

    Args:
        file_path: Path to PDF file

    Returns:
        Number of pages
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except:
        return 0


async def extract_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract PDF metadata.

    Args:
        file_path: Path to PDF file

    Returns:
        PDF metadata dictionary
    """
    result = await parse_pdf(file_path)
    if result.get("success"):
        return result.get("metadata", {})
    return {}


async def search_text_in_pdf(
    file_path: str,
    search_term: str,
    case_sensitive: bool = False
) -> List[Dict[str, Any]]:
    """
    Search for text in PDF.

    Args:
        file_path: Path to PDF file
        search_term: Text to search for
        case_sensitive: Whether search is case sensitive

    Returns:
        List of matches with page numbers and context
    """
    result = await parse_pdf(file_path)
    matches = []

    if not result.get("success"):
        return matches

    for page in result.get("pages", []):
        page_text = page["text"]
        page_num = page["page_number"]

        # Perform search
        if case_sensitive:
            search_text = page_text
            term = search_term
        else:
            search_text = page_text.lower()
            term = search_term.lower()

        if term in search_text:
            # Find all occurrences
            start = 0
            while True:
                pos = search_text.find(term, start)
                if pos == -1:
                    break

                # Extract context (50 chars before and after)
                context_start = max(0, pos - 50)
                context_end = min(len(page_text), pos + len(search_term) + 50)
                context = page_text[context_start:context_end]

                matches.append({
                    "page": page_num,
                    "position": pos,
                    "context": context
                })

                start = pos + 1

    return matches
