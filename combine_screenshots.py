from PIL import Image

# List your screenshot filenames in the order you want them combined
image_files = [
    "assets/a.png",
    "assets/b.png",
    "assets/c.png",
    "assets/d.png",
    "assets/e.png"
]

# Open all images and get their sizes
images = [Image.open(img) for img in image_files]
widths, heights = zip(*(img.size for img in images))

# Calculate the size of the final image
total_height = sum(heights)
max_width = max(widths)

# Create a new blank image with the correct size
combined_img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

# Paste each image into the combined image
y_offset = 0
for img in images:
    combined_img.paste(img, (0, y_offset))
    y_offset += img.height

# Save the result
combined_img.save('assets/screenshot.png')
print("Combined screenshot saved as assets/screenshot.png")
