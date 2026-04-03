# core/metadata_extractor.py
"""
Metadata Extractor — pulls EXIF/document metadata from local files.
Supports: JPEG, PNG, TIFF, DOCX, PDF (basic).
Only processes files you own or have explicit permission to analyze.
"""
import os
from utils.logger import get_logger

logger = get_logger("metadata_extractor")

def extract_image_metadata(filepath: str) -> dict:
    """Extract EXIF metadata from image files using Pillow."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        img = Image.open(filepath)
        raw_exif = img._getexif()
        if not raw_exif:
            return {"note": "No EXIF data found in image."}

        metadata = {}
        for tag_id, value in raw_exif.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = str(value)
        return metadata

    except ImportError:
        return {"error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"error": str(e)}

def extract_docx_metadata(filepath: str) -> dict:
    """Extract metadata from .docx files."""
    try:
        from docx import Document
        doc = Document(filepath)
        props = doc.core_properties
        return {
            "author":         props.author,
            "created":        str(props.created),
            "modified":       str(props.modified),
            "last_modified_by": props.last_modified_by,
            "title":          props.title,
            "subject":        props.subject,
            "description":    props.description,
            "revision":       props.revision,
        }
    except ImportError:
        return {"error": "python-docx not installed. Run: pip install python-docx"}
    except Exception as e:
        return {"error": str(e)}

def extract_metadata(filepath: str) -> dict:
    """Auto-detect file type and extract metadata."""
    if not os.path.isfile(filepath):
        return {"error": f"File not found: {filepath}"}

    ext = os.path.splitext(filepath)[1].lower()
    logger.info(f"Extracting metadata from: {filepath}")

    if ext in (".jpg", ".jpeg", ".png", ".tiff", ".tif"):
        return extract_image_metadata(filepath)
    elif ext == ".docx":
        return extract_docx_metadata(filepath)
    else:
        return {"note": f"Unsupported file type: {ext}. Supported: jpg, png, tiff, docx"}
