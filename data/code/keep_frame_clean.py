from pathlib import Path
import shutil

source = Path(r"D:\piyush\personal_image_generaton\data\insta_data\the_min\frames")
destination = Path(r"D:\piyush\personal_image_generaton\data\insta_data\the_min\process")

destination.mkdir(parents=True, exist_ok=True)

for image_path in source.rglob("*"):
    if image_path.is_file() and image_path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        # Include the relative folder path in the copied name to avoid collisions.
        relative_name = "__".join(image_path.relative_to(source).parts)
        target = destination / relative_name
        shutil.copy2(image_path, target)
        print(f"Copied: {image_path} -> {target}")

print("Done.")