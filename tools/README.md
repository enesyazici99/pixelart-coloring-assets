# Sprite Sheet Splitter Tools

Bu klasör, sprite sheet'lerden bireysel sprite'ları ayıklamak için Python araçları içerir.

## Gereksinimler

```bash
pip install Pillow
```

## Araçlar

### 1. `sprite_splitter.py` - Otomatik Algılama

Transparan arka planlı sprite sheet'lerde sprite'ları **otomatik olarak algılar** ve ayıklar.

**Ne Zaman Kullanılır:**
- Sprite'lar düzensiz yerleştirilmiş
- Sprite'lar farklı boyutlarda
- Transparan arka plan var (PNG)

**Kullanım:**
```bash
python sprite_splitter.py <sprite_sheet.png> [output_dir] [category_name] [max_size]
```

**Örnek:**
```bash
python sprite_splitter.py forest_sprites.png ./forest forest 50
```

**Parametreler:**
- `sprite_sheet.png` - Kaynak sprite sheet dosyası
- `output_dir` - Çıktı klasörü (varsayılan: ./sprites_output)
- `category_name` - Kategori adı, dosya öneki olarak kullanılır (varsayılan: sprite)
- `max_size` - Maksimum sprite boyutu, bundan büyükler atlanır (varsayılan: 50)

---

### 2. `grid_splitter.py` - Grid Tabanlı

Sprite sheet'i **sabit grid boyutuna** göre böler. Düzenli yerleştirilmiş sprite sheet'ler için idealdir.

**Ne Zaman Kullanılır:**
- Sprite'lar düzenli bir grid içinde
- Tüm sprite'lar aynı boyutta (örn: 16x16, 32x32)
- Transparan veya renkli arka plan olabilir

**Kullanım:**
```bash
python grid_splitter.py <sprite_sheet.png> [output_dir] [category_name] [cell_size]
```

**Örnek:**
```bash
python grid_splitter.py items_sheet.png ./items items 16
```

**Parametreler:**
- `sprite_sheet.png` - Kaynak sprite sheet dosyası
- `output_dir` - Çıktı klasörü (varsayılan: ./sprites_output)
- `category_name` - Kategori adı (varsayılan: sprite)
- `cell_size` - Her hücrenin piksel boyutu (varsayılan: 16)

---

## Çıktı Formatı

Her iki araç da aynı çıktı yapısını oluşturur:

```
output_dir/
├── category_001.png
├── category_002.png
├── category_003.png
├── ...
└── meta.json
```

**meta.json örneği:**
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
    },
    ...
  ]
}
```

---

## Yeni Kategori Ekleme Adımları

### 1. Sprite Sheet'i Böl

```bash
cd tools

# Grid tabanlı (örn: 16x16 sprite'lar)
python grid_splitter.py ../input/new_sprites.png ../new_category new_category 16

# VEYA otomatik algılama
python sprite_splitter.py ../input/new_sprites.png ../new_category new_category 50
```

### 2. Çıktıyı Kontrol Et

- Oluşturulan sprite'ları görsel olarak kontrol et
- Gereksiz olanları sil
- `meta.json` dosyasından silinen sprite'ların girdilerini kaldır

### 3. categories.json Güncelle

Ana klasördeki `categories.json` dosyasına yeni kategoriyi ekle:

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

**NOT:** `itemCount` değeri `meta.json`'daki artwork sayısıyla eşleşmeli!

### 4. Git'e Push Et

```bash
git add new_category/ categories.json
git commit -m "Add new_category with X sprites"
git push
```

### 5. CDN URL'ini Güncelle (Opsiyonel)

Eğer cache sorunları yaşanırsa, `pixelart_painter` projesindeki `app_config.dart` dosyasında commit hash'ini güncelle:

```dart
static const String cdnBaseUrl =
    'https://cdn.jsdelivr.net/gh/enesyazici99/pixelart-coloring-assets@COMMIT_HASH';
```

---

## Zorluk Seviyeleri

Araçlar otomatik olarak zorluk seviyesi belirler:

**sprite_splitter.py** (boyuta göre):
- `easy`: ≤256 piksel (16x16)
- `medium`: ≤1024 piksel (32x32)
- `hard`: >1024 piksel

**grid_splitter.py** (renk sayısına göre):
- `easy`: ≤5 renk
- `medium`: 6-10 renk
- `hard`: >10 renk

---

## Filtreleme

### sprite_splitter.py
- Minimum 8x8 piksel (daha küçükler atlanır)
- max_size parametresinden büyükler atlanır
- Yakın sprite'lar otomatik birleştirilir

### grid_splitter.py
- %10'dan az dolu hücreler atlanır (boş kabul edilir)
- Tek renkli hücreler atlanır (solid background)

---

## Sorun Giderme

**"No sprites found"**
- Görüntünün RGBA formatında olduğundan emin ol
- Transparan arka plan varsa sprite_splitter kullan
- min_size veya max_size parametrelerini ayarla

**Sprite'lar birleşiyor**
- sprite_splitter için threshold değerini azalt (kod içinde)
- Grid tabanlı sheet için grid_splitter kullan

**Çok fazla/az sprite çıkıyor**
- max_size parametresini ayarla
- cell_size parametresinin doğru olduğundan emin ol
