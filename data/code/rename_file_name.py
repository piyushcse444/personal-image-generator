from pathlib import Path

folder = Path(r"D:\piyush\personal_image_generaton\data\insta_data\the_min\process")
extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

files = sorted(
    p for p in folder.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
)

# Two-step rename prevents filename collisions.
temporary_files = []
for i, path in enumerate(files, start=1):
    temp = folder / f"__rename_temp_{i:04d}{path.suffix.lower()}"
    path.rename(temp)
    temporary_files.append((temp, i))

for temp, i in temporary_files:
    new_path = folder / f"image_{i:03d}{temp.suffix}"
    temp.rename(new_path)
    print(f"{temp.name} -> {new_path.name}")

print(f"Renamed {len(files)} images.")