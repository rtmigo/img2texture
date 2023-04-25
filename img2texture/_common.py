from PIL import Image

# preventing "Image.DecompressionBombError: Image size (324000000 pixels)
# exceeds limit of 178956970 pixels, could be decompression bomb DOS attack".
# But we are not expecting attacks. Just opening large files
Image.MAX_IMAGE_PIXELS = None
