"""
convert_and_degrade.py

What this does:
1. Converts every PDF in reports_pdf/ into a clean PNG image
   -> saved in reports_images/clean/
2. Takes a random subset of those clean images and creates
   "degraded" versions that simulate real-world phone photos /
   scans (rotation, blur, noise, contrast drop)
   -> saved in reports_images/degraded/
"""

import os
import random
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import cv2

# -----------------------------
# Config
# -----------------------------
PDF_DIR = "reports_pdf"
CLEAN_DIR = os.path.join("reports_images", "clean")
DEGRADED_DIR = os.path.join("reports_images", "degraded")

DEGRADE_SAMPLE_SIZE = 30   # how many PDFs get a degraded version
DEGRADE_FRACTION = 0.2     # fallback: 20% of total if smaller than sample size
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(DEGRADED_DIR, exist_ok=True)


# -----------------------------
# Step 1: PDF -> Clean PNG
# -----------------------------
def convert_pdfs_to_images():
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files in '{PDF_DIR}/'")

    converted = []
    failed = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]  # e.g. P001_Month_1
        output_path = os.path.join(CLEAN_DIR, f"{base_name}.png")

        try:
            # dpi=200 gives good OCR-readable resolution without huge file size
            pages = convert_from_path(pdf_path, dpi=200)
            # our reports are single-page, so just take page 1
            pages[0].save(output_path, "PNG")
            converted.append(base_name)
        except Exception as e:
            failed.append((pdf_file, str(e)))

    print(f"Converted {len(converted)} PDFs to clean PNGs in '{CLEAN_DIR}/'")
    if failed:
        print(f"Failed to convert {len(failed)} files:")
        for name, err in failed:
            print(f"  - {name}: {err}")

    return converted


# -----------------------------
# Step 2: Degradation functions
# -----------------------------
def add_rotation(img, max_angle=6):
    """Simulate a slightly tilted phone photo."""
    angle = random.uniform(-max_angle, max_angle)
    return img.rotate(angle, expand=True, fillcolor="white")


def add_blur(img, radius_range=(1.0, 2.5)):
    """Simulate a slightly out-of-focus camera shot."""
    radius = random.uniform(*radius_range)
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def add_noise(img, intensity=12):
    """Simulate sensor noise / poor lighting graininess."""
    arr = np.array(img).astype(np.int16)
    noise = np.random.randint(-intensity, intensity, arr.shape, dtype=np.int16)
    noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)


def reduce_contrast(img, factor_range=(0.6, 0.8)):
    """Simulate a faded scan / washed-out lighting."""
    factor = random.uniform(*factor_range)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def add_jpeg_compression_artifacts(img, quality=35):
    """Simulate repeated WhatsApp/email compression of a photo."""
    arr = np.array(img.convert("RGB"))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded = cv2.imencode(".jpg", arr, encode_param)
    decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    return Image.fromarray(decoded)


def degrade_image(img):
    """
    Apply a realistic combination of degradations.
    Not every degradation every time -- randomize which ones apply,
    similar to how real-world uploads vary in quality.
    """
    img = img.convert("RGB")

    if random.random() < 0.8:
        img = add_rotation(img)
    if random.random() < 0.7:
        img = reduce_contrast(img)
    if random.random() < 0.6:
        img = add_blur(img)
    if random.random() < 0.5:
        img = add_noise(img)
    if random.random() < 0.7:
        img = add_jpeg_compression_artifacts(img)

    return img


# -----------------------------
# Step 3: Apply degradation to a sample subset
# -----------------------------
def create_degraded_sample(converted_names):
    sample_size = min(DEGRADE_SAMPLE_SIZE, max(1, int(len(converted_names) * DEGRADE_FRACTION)))
    sample_size = min(DEGRADE_SAMPLE_SIZE, len(converted_names)) if len(converted_names) >= DEGRADE_SAMPLE_SIZE else len(converted_names)

    sample = random.sample(converted_names, sample_size)
    print(f"\nCreating degraded versions for {len(sample)} sampled reports...")

    log = []
    for name in sample:
        clean_path = os.path.join(CLEAN_DIR, f"{name}.png")
        degraded_path = os.path.join(DEGRADED_DIR, f"{name}_degraded.png")

        img = Image.open(clean_path)
        degraded = degrade_image(img)
        degraded.save(degraded_path, "PNG")
        log.append(name)

    print(f"Saved {len(log)} degraded images to '{DEGRADED_DIR}/'")

    # save a manifest so you know exactly which files were degraded
    # (you'll need this later to compare clean vs degraded OCR accuracy)
    manifest_path = os.path.join(DEGRADED_DIR, "_degraded_manifest.txt")
    with open(manifest_path, "w") as f:
        for name in log:
            f.write(name + "\n")
    print(f"Manifest of degraded files saved to '{manifest_path}'")

    return log


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    converted = convert_pdfs_to_images()
    if converted:
        create_degraded_sample(converted)
    else:
        print("No PDFs were converted -- check that reports_pdf/ contains .pdf files.")

    print("\nDone.")
    print(f"Clean images:    {CLEAN_DIR}/   ({len(os.listdir(CLEAN_DIR)) if os.path.exists(CLEAN_DIR) else 0} files)")
    print(f"Degraded images: {DEGRADED_DIR}/")