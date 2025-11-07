"""
Image utilities: load, display, encode to base64.

Functions:
- load_image(path) -> PIL.Image
- encode_image_to_base64(image_or_path) -> str
"""

from PIL import Image
import os
import base64
import io
from typing import Union

def load_image(path: str) -> Image.Image:
    """
    Load an image from disk and return a PIL Image object.

    Args:
        path: Path to the image file.

    Raises:
        FileNotFoundError if path doesn't exist or cannot be opened.

    Returns:
        PIL.Image.Image loaded image.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    return Image.open(path)

def encode_image_to_base64(image_or_path: Union[str, Image.Image]) -> str:
    """
    Encode an image (file path or PIL Image) into a base64 string.

    Args:
        image_or_path: Path to an image file or a PIL Image object.

    Returns:
        Base64-encoded string (utf-8) representing the image bytes.
    """
    if isinstance(image_or_path, str):
        if not os.path.exists(image_or_path):
            raise FileNotFoundError(f"Image file not found at: {image_or_path}")
        with open(image_or_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    elif isinstance(image_or_path, Image.Image):
        buffer = io.BytesIO()
        fmt = image_or_path.format or "JPEG"
        image_or_path.save(buffer, format=fmt)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    else:
        raise ValueError("Input must be an image file path or PIL.Image.Image")
