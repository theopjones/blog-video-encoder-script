import os
from PIL import Image
from pathlib import Path

# Ask user for a server path
server_path = input("Please enter the server path: ")

markdown_content = ""

# Traverse the current working directory
for image_path in Path('.').glob("*"):
    # Check if the file is an image
    if image_path.suffix in ['.jpg', '.jpeg', '.png']:
        try:
            # Open an image file
            with Image.open(image_path) as img:
                # Create a thumbnail, with a longest side of 1000 pixels
                img.thumbnail((1000, 1000))
                # Save the thumbnail
                thumbnail_path = image_path.stem + "_thumbnail" + image_path.suffix
                img.save(thumbnail_path)

                # Append to the markdown content
                markdown_content += f'![{thumbnail_path}](https://{server_path}/{image_path}) '
        except Exception as e:
            print(f"Failed to process file {image_path}. Reason: {str(e)}")

# Write markdown file
with open("image_links.md", "w") as md_file:
    md_file.write(markdown_content)

print("Markdown file has been created successfully!")