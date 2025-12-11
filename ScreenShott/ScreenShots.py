import sys
import os
from pathlib import Path
from datetime import datetime
import zipfile
import tempfile

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Missing dependency: Pillow. Install it using:\n  python -m pip install pillow")
    sys.exit(1)

# Try pyautogui first
screenshot_func = None
try:
    import pyautogui

    def _screenshot_with_pyautogui():
        return pyautogui.screenshot()

    screenshot_func = _screenshot_with_pyautogui
except Exception:
    try:
        from PIL import ImageGrab

        def _screenshot_with_imagegrab():
            return ImageGrab.grab()

        screenshot_func = _screenshot_with_imagegrab
    except Exception:
        print("No screenshot method available.")
        sys.exit(1)


def main():
    # Desktop path
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path(os.environ.get("USERPROFILE", Path.home())) / "Desktop"
    if not desktop.exists():
        desktop = Path.home()  # fallback

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_name = f"screenshot_{timestamp}.png"
    zip_name = f"screenshot_{timestamp}.zip"
    final_image_path = desktop / image_name  # Save final image on Desktop
    zip_path = desktop / zip_name

    try:
        # 1) Take screenshot
        img = screenshot_func()
        if not isinstance(img, Image.Image):
            img = Image.fromarray(img)

        # 2) Convert to grayscale
        img_gray = ImageOps.grayscale(img)

        # 3) Flip horizontally
        img_flipped = ImageOps.mirror(img_gray)

        # 4) Save processed image on Desktop
        img_flipped.save(final_image_path, format="PNG")
        print(f"Processed image saved : {final_image_path}")

        # 5) Create ZIP containing the image
        with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(final_image_path, arcname=image_name)

        print(f"ZIP file created : {zip_path}")

    except Exception as e:
        print("Error during execution:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
