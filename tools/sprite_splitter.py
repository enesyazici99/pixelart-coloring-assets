#!/usr/bin/env python3
"""
Sprite Sheet Splitter
Automatically detects and extracts individual sprites from a sprite sheet.
"""

import os
import sys
from PIL import Image
import json

def find_sprites(image, min_size=8, padding=1):
    """
    Find individual sprites in an image by detecting connected non-transparent regions.
    Returns a list of bounding boxes (left, top, right, bottom).
    """
    width, height = image.size
    pixels = image.load()
    visited = set()
    sprites = []

    def is_transparent(x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return True
        pixel = pixels[x, y]
        # Check alpha channel (RGBA)
        if len(pixel) == 4:
            return pixel[3] < 128
        return False

    def flood_fill(start_x, start_y):
        """Find the bounding box of a connected region."""
        stack = [(start_x, start_y)]
        min_x, min_y = start_x, start_y
        max_x, max_y = start_x, start_y

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            if is_transparent(x, y):
                continue

            visited.add((x, y))
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

            # Check 8-connected neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited and not is_transparent(nx, ny):
                        stack.append((nx, ny))

        return (min_x, min_y, max_x + 1, max_y + 1)

    # Scan the image for sprites
    for y in range(height):
        for x in range(width):
            if (x, y) not in visited and not is_transparent(x, y):
                bbox = flood_fill(x, y)
                sprite_width = bbox[2] - bbox[0]
                sprite_height = bbox[3] - bbox[1]

                # Filter out tiny sprites (noise)
                if sprite_width >= min_size and sprite_height >= min_size:
                    sprites.append(bbox)

    # Merge overlapping or very close sprites
    merged = merge_close_sprites(sprites, threshold=2)

    return merged

def merge_close_sprites(sprites, threshold=2):
    """Merge sprites that are very close together."""
    if not sprites:
        return sprites

    merged = list(sprites)
    changed = True

    while changed:
        changed = False
        new_merged = []
        used = set()

        for i, box1 in enumerate(merged):
            if i in used:
                continue

            current = box1
            for j, box2 in enumerate(merged):
                if j <= i or j in used:
                    continue

                # Check if boxes overlap or are very close
                if boxes_overlap(current, box2, threshold):
                    # Merge the boxes
                    current = (
                        min(current[0], box2[0]),
                        min(current[1], box2[1]),
                        max(current[2], box2[2]),
                        max(current[3], box2[3])
                    )
                    used.add(j)
                    changed = True

            new_merged.append(current)
            used.add(i)

        merged = new_merged

    return merged

def boxes_overlap(box1, box2, threshold=0):
    """Check if two boxes overlap or are within threshold distance."""
    return not (
        box1[2] + threshold < box2[0] or
        box2[2] + threshold < box1[0] or
        box1[3] + threshold < box2[1] or
        box2[3] + threshold < box1[1]
    )

def extract_and_save_sprites(image_path, output_dir, category_name="woods", min_size=8, max_size=50):
    """
    Extract sprites from a sprite sheet and save them as individual files.
    Also generates a meta.json file for the game.
    """
    # Load image
    image = Image.open(image_path).convert("RGBA")
    print(f"Loaded image: {image.size[0]}x{image.size[1]}")

    # Find sprites
    all_sprites = find_sprites(image, min_size=min_size)
    print(f"Found {len(all_sprites)} total sprites")

    # Filter by max size
    sprites = []
    for bbox in all_sprites:
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= max_size and height <= max_size:
            sprites.append(bbox)
        else:
            print(f"  Skipping sprite {width}x{height} (too large)")

    print(f"Keeping {len(sprites)} sprites (max {max_size}x{max_size})")

    # Sort sprites by position (top-left to bottom-right)
    sprites.sort(key=lambda b: (b[1] // 20, b[0]))

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Extract and save each sprite
    artworks = []
    for i, bbox in enumerate(sprites):
        sprite = image.crop(bbox)
        sprite_width = bbox[2] - bbox[0]
        sprite_height = bbox[3] - bbox[1]

        # Generate filename
        filename = f"{category_name}_{i+1:02d}.png"
        filepath = os.path.join(output_dir, filename)

        # Save sprite
        sprite.save(filepath, "PNG")

        # Count unique colors (excluding transparent)
        colors = set()
        for y in range(sprite.height):
            for x in range(sprite.width):
                pixel = sprite.getpixel((x, y))
                if len(pixel) == 4 and pixel[3] >= 128:
                    # Quantize colors slightly to reduce count
                    r = (pixel[0] // 8) * 8
                    g = (pixel[1] // 8) * 8
                    b = (pixel[2] // 8) * 8
                    colors.add((r, g, b))

        # Determine difficulty based on size and colors
        total_cells = sprite_width * sprite_height
        if total_cells <= 256:
            difficulty = "easy"
        elif total_cells <= 1024:
            difficulty = "medium"
        else:
            difficulty = "hard"

        artwork = {
            "id": f"{category_name[0]}{i+1}",
            "name": f"{category_name.title()} {i+1}",
            "filename": filename,
            "colors": len(colors),
            "difficulty": difficulty,
            "width": sprite_width,
            "height": sprite_height
        }
        artworks.append(artwork)

        print(f"  {filename}: {sprite_width}x{sprite_height}, {len(colors)} colors, {difficulty}")

    # Generate meta.json
    meta = {"artworks": artworks}
    meta_path = os.path.join(output_dir, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"\nSaved {len(sprites)} sprites to {output_dir}")
    print(f"Generated meta.json")

    return artworks

def main():
    if len(sys.argv) < 2:
        print("Usage: python sprite_splitter.py <sprite_sheet.png> [output_dir] [category_name] [max_size]")
        print("Example: python sprite_splitter.py woods.png ./output woods 50")
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./sprites_output"
    category_name = sys.argv[3] if len(sys.argv) > 3 else "sprite"
    max_size = int(sys.argv[4]) if len(sys.argv) > 4 else 50

    extract_and_save_sprites(image_path, output_dir, category_name, max_size=max_size)

if __name__ == "__main__":
    main()
