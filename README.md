# Pixelart Coloring Assets

Pixel art assets for the Pixelart Painter app.

## Structure

```
├── categories.json          # List of all categories
├── animals/
│   ├── meta.json           # List of artworks in this category
│   └── *.png               # Pixel art PNG files
├── nature/
│   ├── meta.json
│   └── *.png
├── landscapes/
│   ├── meta.json
│   └── *.png
└── vehicles/
    ├── meta.json
    └── *.png
```

## Adding New Artwork

1. Add your pixel art PNG to the appropriate category folder
2. Update the category's `meta.json`:

```json
{
  "items": [
    {
      "id": "my_artwork",
      "name": "My Artwork",
      "file": "my_artwork.png",
      "premium": false
    }
  ]
}
```

3. Update `itemCount` in `categories.json`

## Requirements

- PNG format
- Recommended sizes: 16x16, 32x32, 48x48, 64x64
- Max 15-20 colors per image for best user experience
- No transparency (or minimal transparency)
