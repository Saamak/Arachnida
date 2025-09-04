import os
import sys
from datetime import datetime  # To format dates
from PIL import Image, ExifTags # To read image metadata

def scorpion():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    for filepath in sys.argv[1:]:
        # First, check if the file exists
        if not os.path.isfile(filepath):
            print(f"Error: File '{filepath}' not found.")
            continue  # Move to the next one

        # Then, check the extension
        if filepath.lower().endswith(allowed_extensions):
            print(f"Analyzing {filepath}...")
            # The rest of your logic for analyzing the file will go here
            print("\n[File]")
            try:
                size_bytes = os.path.getsize(filepath)
                print(f"  Size        : {size_bytes / 1024:.2f} KB") # Display in KB

                # Modification date:
                modif_time = os.path.getmtime(filepath)
                print(f"  Modified on : {datetime.fromtimestamp(modif_time).strftime('%Y-%m-%d %H:%M:%S')}")
            except OSError as e:
                print(f"  Error reading file attributes: {e}")
            print("\n[Image]")
            try:
                img = Image.open(filepath)
                # Basic attributes
                print(f"  Format      : {img.format}")
                print(f"  Dimensions  : {img.width}x{img.height} pixels")
                print(f"  Color mode  : {img.mode}")

                # Readable EXIF data
                exif_data_raw = img._getexif()
                if exif_data_raw:
                    print("\n[EXIF Data]")
                    for key, val in exif_data_raw.items():
                        tag_name = ExifTags.TAGS.get(key, key)
                        # Check if the value is a bytes object to avoid printing raw binary data
                        if isinstance(val, bytes): # if value is in binary
                            print(f"  {tag_name}: <Binary data of length {len(val)}>")
                        else:
                            print(f"  {tag_name}: {val}")
                else:
                    # If exif_data_raw is None, indicate it
                    print("[EXIF Data]: No EXIF data found.")
            except OSError as e:
                print(f"  Error reading image attributes: {e}")

        else:
            print(f"Error: The extension of '{filepath}' is not supported.")

if __name__ == "__main__":
    scorpion()
