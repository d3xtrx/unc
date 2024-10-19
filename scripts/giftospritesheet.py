#!/usr/bin/env python3
from os import listdir
from PIL import Image
import sys

OUTPUT_SIZE_HOZ = 64
OUTPUT_SIZE_VER = 64
MONOCHROME = False 

gif_files = [file for file in listdir() if file.endswith('.gif')]

if not gif_files:
    print("No GIF files found in the current directory.")
    sys.exit(1)

for file in gif_files:
    try:
        with Image.open(file) as gif:
            print(f"Processing {file}")
            print(f"Size: {gif.size}")
            print(f"Frames: {gif.n_frames}")

            if MONOCHROME:
                output = Image.new("1", (OUTPUT_SIZE_HOZ * gif.n_frames, OUTPUT_SIZE_VER), 0)
            else:
                output = Image.new("RGB", (OUTPUT_SIZE_HOZ * gif.n_frames, OUTPUT_SIZE_VER))

            output_filename = f"icon_{gif.n_frames}_frames.bmp"

            for frame in range(0, gif.n_frames):
                gif.seek(frame)
                extracted_frame = gif.convert("RGB")
                extracted_frame = extracted_frame.resize((OUTPUT_SIZE_HOZ, OUTPUT_SIZE_VER))
                position = (OUTPUT_SIZE_HOZ * frame, 0)
                output.paste(extracted_frame, position)

            if not MONOCHROME:
                output = output.convert("P", colors=8)
            output.save(output_filename)
            print(f"Saved {output_filename}")

    except Exception as e:
        print(f"Error processing {file}: {str(e)}")

print("Processing complete.")