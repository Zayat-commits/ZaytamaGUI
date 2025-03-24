import os
import sys
from PyQt6.QtGui import QPixmap, QImage, QGuiApplication
import time

def get_last_processed_date(file_path="last_preprocessing.txt"):
    """ Get the last processed date from file. """
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return "1970-01-01"  # Default to an old date if no file exists

def save_last_processed_date(file_path="last_preprocessing.txt"):
    """ Save the current date as the last processed date. """
    current_date = time.strftime("%Y-%m-%d")
    with open(file_path, "w") as f:
        f.write(current_date)

def preprocess_image(image_path, target_height=500):
    original_pixmap = QPixmap(image_path)
    if original_pixmap.isNull():
        print(f"Error: Could not load image from {image_path}")
        return None

    image = original_pixmap.toImage()
    width, height = image.width(), image.height()

    # Crop out transparent pixels vertically
    min_y, max_y = None, None
    for y in range(height):
        for x in range(width):
            if image.pixelColor(x, y).alpha() > 0:  # Found a non-transparent pixel
                if min_y is None:
                    min_y = y  # First row with color (top)
                max_y = y  # Last row with color (bottom)

    if None in (min_y, max_y):  
        return original_pixmap  # Return original if fully transparent

    # Crop the image vertically
    cropped_pixmap = original_pixmap.copy(0, min_y, width, max_y - min_y)

    # Resize while maintaining aspect ratio (only vertically)
    aspect_ratio = cropped_pixmap.width() / cropped_pixmap.height()
    new_width = int(target_height * aspect_ratio)
    final_pixmap = cropped_pixmap.scaled(new_width, target_height)

    return final_pixmap  # Return processed image

def preprocess_images_in_folder(folder_path, target_height=500, last_processed_date=None):
    # Get all PNG files in the folder
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Sort the images by modification date
    image_paths.sort(key=lambda x: os.path.getmtime(x))  # Sort by last modified time

    for image_path in image_paths:
        # Get modification date of the image
        mod_time = time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(image_path)))
        
        # Process only if image was modified after the last processed date
        if mod_time > last_processed_date:
            print(f"Processing image: {image_path}")
            processed_pixmap = preprocess_image(image_path, target_height)
            if processed_pixmap:
                processed_pixmap.save(image_path)  # Overwrite the original image

# Initialize QGuiApplication before using QPixmap
app = QGuiApplication(sys.argv)

# Get the last processed date (from the saved file)
last_processed_date = get_last_processed_date()

# Run preprocessing only on the new images
preprocess_images_in_folder("Physique", last_processed_date=last_processed_date)

# After processing, save the current date as the new "last processed date"
save_last_processed_date()
