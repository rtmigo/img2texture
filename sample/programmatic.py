from PIL import Image
from img2texture import image_to_seamless

# load PIL image
src_image = Image.open("/path/to/source.png")

# convert to seamless PIL image
result_image = image_to_seamless(src_image, overlap=0.1)

# save
result_image.save("/path/to/result.png")