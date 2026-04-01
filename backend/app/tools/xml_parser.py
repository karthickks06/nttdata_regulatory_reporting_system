"""XML parsing tool"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import xml.etree.ElementTree as ET
from lxml import etree


async def parse_xml(file_path: str) -> Dict[str, Any]:
    """
    Parse XML file and extract structure and content.

    Args:
        file_path: Path to XML file

    Returns:
        Dictionary containing parsed XML data
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract text content
        text_content = " ".join(root.itertext())

        # Build structure
        structure = _element_to_dict(root)

        # Extract all elements
        elements = []
        for elem in root.iter():
            elements.append({
                "tag": elem.tag,
                "text": elem.text.strip() if elem.text else "",
                "attributes": dict(elem.attrib)
            })

        return {
            "success": True,
            "root_tag": root.tag,
            "text": text_content,
            "structure": structure,
            "elements": elements,
            "element_count": len(elements)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }


def _element_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Convert XML element to dictionary"""
    result = {
        "tag": element.tag,
        "attributes": dict(element.attrib)
    }

    # Add text if present
    if element.text and element.text.strip():
        result["text"] = element.text.strip()

    # Add children
    children = []
    for child in element:
        children.append(_element_to_dict(child))

    if children:
        result["children"] = children

    return result


async def parse_xml_with_xpath(
    file_path: str,
    xpath_queries: List[str]
) -> Dict[str, Any]:
    """
    Parse XML and extract data using XPath queries.

    Args:
        file_path: Path to XML file
        xpath_queries: List of XPath queries

    Returns:
        Query results
    """
    try:
        tree = etree.parse(file_path)

        results = {}
        for query in xpath_queries:
            elements = tree.xpath(query)

            query_results = []
            for elem in elements:
                if isinstance(elem, str):
                    query_results.append(elem)
                elif hasattr(elem, 'tag'):
                    query_results.append({
                        "tag": elem.tag,
                        "text": elem.text,
                        "attributes": dict(elem.attrib)
                    })

            results[query] = query_results

        return {
            "success": True,
            "queries": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def validate_xml_schema(
    file_path: str,
    schema_path: str
) -> Dict[str, Any]:
    """
    Validate XML against XSD schema.

    Args:
        file_path: Path to XML file
        schema_path: Path to XSD schema file

    Returns:
        Validation result
    """
    try:
        # Parse schema
        with open(schema_path, 'rb') as schema_file:
            schema_root = etree.XML(schema_file.read())
            schema = etree.XMLSchema(schema_root)

        # Parse XML
        with open(file_path, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)

        # Validate
        is_valid = schema.validate(xml_doc)

        result = {
            "success": True,
            "is_valid": is_valid
        }

        if not is_valid:
            result["errors"] = [
                {"message": str(error)}
                for error in schema.error_log
            ]

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def xml_to_json(file_path: str) -> Dict[str, Any]:
    """
    Convert XML file to JSON structure.

    Args:
        file_path: Path to XML file

    Returns:
        JSON representation of XML
    """
    result = await parse_xml(file_path)

    if result.get("success"):
        return {
            "success": True,
            "json": result.get("structure", {})
        }

    return result


async def extract_xml_elements_by_tag(
    file_path: str,
    tag_name: str
) -> List[Dict[str, Any]]:
    """
    Extract all elements with specific tag name.

    Args:
        file_path: Path to XML file
        tag_name: Tag name to search for

    Returns:
        List of matching elements
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        elements = []
        for elem in root.iter(tag_name):
            elements.append({
                "tag": elem.tag,
                "text": elem.text.strip() if elem.text else "",
                "attributes": dict(elem.attrib)
            })

        return elements

    except Exception as e:
        return []
