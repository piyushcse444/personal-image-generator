from pathlib import Path
from itertools import combinations
import csv

import cv2
import imagehash
from PIL import Image, ImageOps

SOURCE = Path(r"D:\piyush\personal_image_generaton\data\insta_data\the_min\process")
REPORT = SOURCE / "image_review_report.csv"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Tune this after reviewing results:
BLUR_THRESHOLD = 80
DUPLICATE_HASH_DISTANCE = 6

# OpenCV's built-in face detector. It is a useful first pass, not perfect.
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(cascade_path)

images = sorted(
    p for p in SOURCE.rglob("*")
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
)

results = []

for path in images:
    try:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            width, height = image.size
            phash = imagehash.phash(image)

            gray = cv2.cvtColor(
                cv2.imread(str(path)),
                cv2.COLOR_BGR2GRAY
            )
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            flags = []
            if blur_score < BLUR_THRESHOLD:
                flags.append("possibly_blurry")
            if len(faces) == 0:
                flags.append("no_face_detected_check_manually")
            elif len(faces) > 1:
                flags.append("multiple_faces")

            results.append({
                "path": str(path),
                "width": width,
                "height": height,
                "blur_score": round(float(blur_score), 2),
                "face_count": len(faces),
                "phash": str(phash),
                "duplicate_of": "",
                "flags": ";".join(flags),
            })

    except Exception as error:
        results.append({
            "path": str(path),
            "width": "",
            "height": "",
            "blur_score": "",
            "face_count": "",
            "phash": "",
            "duplicate_of": "",
            "flags": f"could_not_read: {error}",
        })

# Mark likely duplicates. The first matching image is kept as the reference.
valid = [r for r in results if r["phash"]]
for first, second in combinations(valid, 2):
    distance = imagehash.hex_to_hash(first["phash"]) - imagehash.hex_to_hash(second["phash"])
    if distance <= DUPLICATE_HASH_DISTANCE:
        second["duplicate_of"] = first["path"]
        existing = second["flags"]
        second["flags"] = (existing + ";" if existing else "") + "possible_duplicate"

with REPORT.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "path", "width", "height", "blur_score",
        "face_count", "duplicate_of", "flags"
    ])
    writer.writeheader()
    for row in results:
        writer.writerow({key: row[key] for key in writer.fieldnames})

print(f"Checked {len(images)} images.")
print(f"Report saved to: {REPORT}")