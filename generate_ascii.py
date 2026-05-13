"""
Genera ASCII art portrait (dark + light GIF) da una foto.
Uso: python3 generate_ascii.py foto.jpg
Output: assets/ascii-dark.gif  assets/ascii-light.gif
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import math

# Caratteri ASCII dal più denso al più leggero
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(img, cols=120, scale=0.55):
    width, height = img.size
    cell_w = width / cols
    cell_h = cell_w / scale
    rows = int(height / cell_h)
    
    img_gray = img.convert("L")
    img_resized = img_gray.resize((cols, rows))
    
    lines = []
    for row in range(rows):
        line = ""
        for col in range(cols):
            pixel = img_resized.getpixel((col, row))
            idx = int(pixel / 255 * (len(ASCII_CHARS) - 1))
            line += ASCII_CHARS[idx]
        lines.append(line)
    return lines

def ascii_to_image(lines, dark_mode=True, font_size=10):
    bg_color = (13, 17, 23) if dark_mode else (255, 255, 255)
    text_color = (230, 230, 230) if dark_mode else (20, 20, 20)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calcola dimensioni
    dummy = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), "A", font=font)
    char_w = bbox[2] - bbox[0]
    char_h = bbox[3] - bbox[1] + 2
    
    img_w = char_w * len(lines[0])
    img_h = char_h * len(lines)
    
    img = Image.new("RGB", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(img)
    
    for i, line in enumerate(lines):
        draw.text((0, i * char_h), line, fill=text_color, font=font)
    
    return img

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 generate_ascii.py tua_foto.jpg")
        sys.exit(1)
    
    input_path = sys.argv[1]
    os.makedirs("assets", exist_ok=True)
    
    img = Image.open(input_path)
    
    # Crop al centro (focus sul viso/busto)
    w, h = img.size
    crop_h = int(h * 0.85)
    img = img.crop((0, 0, w, crop_h))
    
    lines = image_to_ascii(img, cols=100, scale=0.5)
    
    # Dark mode
    dark_img = ascii_to_image(lines, dark_mode=True, font_size=9)
    dark_img.save("assets/ascii-dark.gif")
    print("✓ assets/ascii-dark.gif generato")
    
    # Light mode
    light_img = ascii_to_image(lines, dark_mode=False, font_size=9)
    light_img.save("assets/ascii-light.gif")
    print("✓ assets/ascii-light.gif generato")
    
    print("\nOra carica la cartella assets/ su GitHub insieme al README.md")
