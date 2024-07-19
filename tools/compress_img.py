import os
from PIL import Image

def get_optimal_size(image_path, max_size=2*1024*1024):
    """
    Calculate the optimal size to compress the image to fit within the max_size.
    """
    img = Image.open(image_path)
    width, height = img.size
    current_size = os.path.getsize(image_path)

    if current_size <= max_size:
        return width, height

    # Calculate the new dimensions while preserving the aspect ratio
    while True:
        width = int(width * 0.9)  # Reduce by 10% each iteration
        height = int(height * 0.9)
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        img_resized.save(image_path, optimize=True, quality=95)
        new_size = os.path.getsize(image_path)
        if new_size <= max_size:
            return width, height

def compress_image(image_path):
    """
    Compress an image to fit within 2MB while maintaining its aspect ratio.
    """
    try:
        optimal_width, optimal_height = get_optimal_size(image_path)
        img = Image.open(image_path)
        img = img.convert('RGB') if img.mode != 'RGB' else img  # Ensure image is in RGB mode
        img = img.resize((optimal_width, optimal_height), Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=95)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def traverse_directory(directory):
    """
    Traverse a directory and its subdirectories to find and compress all images.
    """
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg')):
                image_path = os.path.join(foldername, filename)
                compress_image(image_path)


# Specify the directory you want to start from
root_directory = '/Users/colaforced/code_space/imgs'
traverse_directory(root_directory)