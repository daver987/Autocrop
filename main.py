from PIL import Image
import os


def is_white(image, x, y, color_tolerance=50):
    pixel = image.getpixel((x, y))
    reference_color = (237, 237, 212)  # Color #EEDED4 in RGB
    return all(
        abs(value - ref_value) <= color_tolerance
        for value, ref_value in zip(pixel, reference_color)
    )


def auto_crop(image_path, output_path):
    image = Image.open(image_path).convert("RGB")  # Ensure image is in RGB mode
    width, height = image.size

    # Find left border
    left = 0
    for x in range(width):
        for y in range(height):
            if not is_white(image, x, y):
                left = x
                break
        if left > 0:
            break

    # Find right border
    right = width - 1
    for x in range(width - 1, -1, -1):
        for y in range(height):
            if not is_white(image, x, y):
                right = x
                break
        if right < width - 1:
            break

    # Find top border
    top = 0
    for y in range(height):
        for x in range(width):
            if not is_white(image, x, y):
                top = y
                break
        if top > 0:
            break

    # Find bottom border
    bottom = height - 1
    for y in range(height - 1, -1, -1):
        for x in range(width):
            if not is_white(image, x, y):
                bottom = y
                break
        if bottom < height - 1:
            break

    cropped_image = image.crop((left, top, right + 1, bottom + 1))
    cropped_image.save(output_path, quality=100)


# Example usage
input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    # Check if the file is an image (you can add more file extensions if needed)
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        auto_crop(input_path, output_path)
