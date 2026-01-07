import numpy as np
from PIL import Image

def array_to_grayscale_image(arr, output_path):
    # 如果数组是0-1范围的浮点数，需要先转换
    if arr.dtype == np.float64 or arr.dtype == np.float32:
        arr = (arr * 255).astype(np.uint8)
    img = Image.fromarray(arr, mode='L')
    img.save(output_path)

def grayscale_image_to_array(image_path):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    return arr
