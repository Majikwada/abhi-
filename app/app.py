from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

APP_ROOT = Path(__file__).resolve().parent
GENERATED_DIR = APP_ROOT / "generated"

app = Flask(__name__)


SPAM_KEYWORDS = {
    "free",
    "winner",
    "cash",
    "urgent",
    "act now",
    "limited time",
    "click",
    "subscribe",
    "buy now",
    "guaranteed",
    "offer",
    "prize",
    "bitcoin",
}


def detect_spam(message: str) -> bool:
    normalized = message.lower()
    return any(keyword in normalized for keyword in SPAM_KEYWORDS)


def generate_result_image(message: str, is_spam: bool) -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    status_text = "SPAM" if is_spam else "NOT SPAM"
    subtitle = "Auto-generated preview"

    image = Image.new("RGB", (900, 500), (248, 250, 252))
    draw = ImageDraw.Draw(image)

    title_color = (220, 38, 38) if is_spam else (22, 163, 74)
    body_color = (30, 41, 59)
    label_color = (100, 116, 139)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    draw.text((60, 60), status_text, font=title_font, fill=title_color)
    draw.text((60, 150), subtitle, font=label_font, fill=label_color)

    preview = message.strip() or "(no message provided)"
    preview_lines = []
    max_chars = 60
    while preview:
        preview_lines.append(preview[:max_chars])
        preview = preview[max_chars:]

    y_offset = 220
    for line in preview_lines[:6]:
        draw.text((60, y_offset), line, font=body_font, fill=body_color)
        y_offset += 36

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    output_path = GENERATED_DIR / f"result_{timestamp}.png"
    image.save(output_path)
    return output_path


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    is_spam = None
    image_path = None
    if request.method == "POST":
        message = request.form.get("message", "")
        is_spam = detect_spam(message)
        image_path = generate_result_image(message, is_spam)
    return render_template(
        "index.html",
        message=message,
        is_spam=is_spam,
        image_path=image_path.name if image_path else None,
    )


@app.route("/generated/<filename>")
def generated_file(filename: str):
    file_path = GENERATED_DIR / filename
    return send_file(file_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
