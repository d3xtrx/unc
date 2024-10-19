#!/usr/bin/env python3
from os import listdir, system
from PIL import Image
import sys
from pygifsicle import optimize



gif_files = [file for file in listdir() if file.endswith('.gif')]

for file in gif_files:
    optimize(file)
    with Image.open(file) as gif:
        print(f"Processing {file}")
        width, height = gif.size
        print(f"Size: {gif.size}")
        print(f"Frames: {gif.n_frames}")
        output = Image.new("RGB", (width * gif.n_frames, height))
        output_filename = f"{file}_{gif.n_frames}_frames.bmp"
        for frame in range(0, gif.n_frames):
            gif.seek(frame)
            extracted_frame = gif.convert("RGB")
            extracted_frame = extracted_frame.resize((width, height))
            position = (width * frame, 0)
            output.paste(extracted_frame, position)
        output.save(output_filename)
        system("magick " + str({output_filename}) +" -type palette -compress RLE " + str({output_filename}))
        print(f"Saved {output_filename}")
