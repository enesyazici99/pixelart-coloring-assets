# Pixelart Coloring Assets

Pixel art assets for the Pixelart Painter app.

## Structure

```
├── categories.json          # List of all categories
├── tools/                   # Sprite extraction tools
│   ├── sprite_splitter.py  # Auto-detect sprites
│   ├── grid_splitter.py    # Grid-based splitting
│   └── README.md           # Tool documentation
├── forest/
│   ├── meta.json           # List of artworks
│   └── *.png               # Pixel art files
├── items/
│   ├── meta.json
│   └── *.png
├── animals/
│   ├── meta.json
│   └── *.png
└── ...
```

## Quick Start: Adding a New Category

### 1. Extract Sprites from Sheet

```bash
cd tools
pip install Pillow

# For grid-based sheets (e.g., 16x16 sprites)
python grid_splitter.py ../input/sheet.png ../new_category new_category 16

# For transparent background sheets
python sprite_splitter.py ../input/sheet.png ../new_category new_category 50
```

### 2. Update categories.json

```json
{
  "categories": [
    ...
    {
      "id": "new_category",
      "name": "New Category",
      "icon": "new_category_icon",
      "itemCount": 50,
      "premium": false
    }
  ]
}
```

### 3. Push Changes

```bash
git add new_category/ categories.json
git commit -m "Add new_category"
git push
```

See [tools/README.md](tools/README.md) for detailed documentation.

## meta.json Format

```json
{
  "artworks": [
    {
      "id": "c1",
      "name": "Category 1",
      "filename": "category_001.png",
      "colors": 8,
      "difficulty": "easy",
      "width": 16,
      "height": 16
    }
  ]
}
```

## Requirements

- PNG format
- Recommended sizes: 16x16, 32x32, 48x48, 64x64
- Max 15-20 colors per image for best user experience
- Transparent background preferred

## CDN URL

Assets are served via jsDelivr:

```
https://cdn.jsdelivr.net/gh/enesyazici99/pixelart-coloring-assets@main/{category}/{file}
```

To bypass cache after updates, use commit hash instead of `@main`:

```
https://cdn.jsdelivr.net/gh/enesyazici99/pixelart-coloring-assets@COMMIT_HASH/{category}/{file}
```
