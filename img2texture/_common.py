from PIL import Image

# preventing Image.DecompressionBombError: Image size (324000000 pixels)
# exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.
# We just open a large file and are not afraid of it
Image.MAX_IMAGE_PIXELS = None
