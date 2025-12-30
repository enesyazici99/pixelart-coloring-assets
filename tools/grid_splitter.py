#!/usr/bin/env python3
"""
Grid-based Sprite Sheet Splitter
Splits a sprite sheet into individual sprites based on a fixed grid size.
"""

import os
import sys
from PIL import Image
import json

def split_grid(image_path, output_dir, category_name, cell_size=16, padding=0):
    """
    Split a sprite sheet into individual sprites based on a grid.

    Args:
        image_path: Path to the sprite sheet
        output_dir: Directory to save extracted sprites
        category_name: Category name for the sprites
        cell_size: Size of each cell in the grid (default 16x16)
        padding: Padding between cells (default 0)
    """
    # Load image
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    print(f"Loaded image: {width}x{height}")

    # Calculate grid dimensions
    step = cell_size + padding
    cols = width // step
    rows = height // step
    print(f"Grid: {cols} columns x {rows} rows = {cols * rows} cells")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    artworks = []
    sprite_index = 1

    for row in range(rows):
        for col in range(cols):
            # Calculate crop box
            left = col * step
            top = row * step
            right = left + cell_size
            bottom = top + cell_size

            # Crop the sprite
            sprite = image.crop((left, top, right, bottom))

            # Check if sprite has any non-transparent content
            pixels = list(sprite.getdata())
            non_transparent = sum(1 for p in pixels if len(p) == 4 and p[3] > 128)

            # Skip empty sprites (less than 10% non-transparent)
            if non_transparent < (cell_size * cell_size * 0.1):
                continue

            # Count unique colors
            colors = set()
            for pixel in pixels:
                if len(pixel) == 4 and pixel[3] > 128:
                    r = (pixel[0] // 16) * 16
                    g = (pixel[1] // 16) * 16
                    b = (pixel[2] // 16) * 16
                    colors.add((r, g, b))

            # Skip sprites with only 1 color (probably solid background)
            if len(colors) < 2:
                continue

            # Save sprite
            filename = f"{category_name}_{sprite_index:03d}.png"
            filepath = os.path.join(output_dir, filename)
            sprite.save(filepath, "PNG")

            # Determine difficulty
            if len(colors) <= 5:
                difficulty = "easy"
            elif len(colors) <= 10:
                difficulty = "medium"
            else:
                difficulty = "hard"

            artwork = {
                "id": f"{category_name[0]}{sprite_index}",
                "name": f"{category_name.title()} {sprite_index}",
                "filename": filename,
                "colors": len(colors),
                "difficulty": difficulty,
                "width": cell_size,
                "height": cell_size
            }
            artworks.append(artwork)

            if sprite_index <= 10 or sprite_index % 50 == 0:
                print(f"  {filename}: {len(colors)} colors, {difficulty}")

            sprite_index += 1

    # Generate meta.json
    meta = {"artworks": artworks}
    meta_path = os.path.join(output_dir, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"\nSaved {len(artworks)} sprites to {output_dir}")
    print(f"Generated meta.json")

    return artworks

def main():
    if len(sys.argv) < 2:
        print("Usage: python grid_splitter.py <sprite_sheet.png> [output_dir] [category_name] [cell_size]")
        print("Example: python grid_splitter.py items.png ./output items 16")
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./sprites_output"
    category_name = sys.argv[3] if len(sys.argv) > 3 else "sprite"
    cell_size = int(sys.argv[4]) if len(sys.argv) > 4 else 16

    split_grid(image_path, output_dir, category_name, cell_size)

if __name__ == "__main__":
    main()
