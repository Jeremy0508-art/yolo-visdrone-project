import sys
import uuid
from pathlib import Path

import cv2
from flask import Flask, flash, redirect, render_template, request, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.register import register_custom_modules
from src.utils.paths import resolve_project_path


WEB_ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = WEB_ROOT / "uploads"
RESULT_DIR = WEB_ROOT / "static" / "results"
DEFAULT_WEIGHTS = resolve_project_path("runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

MODEL: YOLO | None = None


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "yolo-visdrone-local"
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    @app.get("/")
    def index():
        return render_template("index.html", default_conf=0.25, weights_path=DEFAULT_WEIGHTS)

    @app.post("/detect")
    def detect():
        uploaded = request.files.get("file")
        if uploaded is None or uploaded.filename == "":
            flash("Please choose an image or video file.")
            return redirect(url_for("index"))

        original_name = secure_filename(uploaded.filename)
        suffix = Path(original_name).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            flash("Unsupported file type.")
            return redirect(url_for("index"))

        conf = parse_confidence(request.form.get("conf", "0.25"))
        job_id = uuid.uuid4().hex[:12]
        upload_path = UPLOAD_DIR / f"{job_id}_{original_name}"
        uploaded.save(upload_path)

        result_path = run_detection(upload_path, job_id, conf)
        media_type = "video" if suffix in VIDEO_EXTENSIONS else "image"
        display_path = to_static_result_path(result_path)
        return render_template(
            "index.html",
            default_conf=conf,
            weights_path=DEFAULT_WEIGHTS,
            result_path=display_path,
            media_type=media_type,
            original_name=original_name,
        )

    return app


def parse_confidence(raw_value: str) -> float:
    try:
        return min(max(float(raw_value), 0.01), 0.95)
    except ValueError:
        return 0.25


def get_model() -> YOLO:
    global MODEL
    if MODEL is None:
        register_custom_modules()
        MODEL = YOLO(str(DEFAULT_WEIGHTS))
    return MODEL


def run_detection(source_path: Path, job_id: str, conf: float) -> Path:
    result_name = f"job_{job_id}"
    model = get_model()
    model.predict(
        source=str(source_path),
        imgsz=640,
        conf=conf,
        project=str(RESULT_DIR),
        name=result_name,
        save=True,
        exist_ok=True,
    )

    result_folder = RESULT_DIR / result_name
    output_path = find_prediction_output(result_folder, source_path)
    if source_path.suffix.lower() in VIDEO_EXTENSIONS:
        output_path = ensure_browser_video(output_path)
    return output_path


def find_prediction_output(result_folder: Path, source_path: Path) -> Path:
    expected = result_folder / source_path.name
    if expected.exists():
        return expected

    source_stem = source_path.stem
    candidates = [path for path in result_folder.iterdir() if path.is_file() and path.stem == source_stem]
    if candidates:
        return candidates[0]

    files = [path for path in result_folder.iterdir() if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS]
    if not files:
        raise FileNotFoundError(f"No prediction output found in {result_folder}")
    return files[0]


def ensure_browser_video(video_path: Path) -> Path:
    if video_path.suffix.lower() == ".mp4":
        return video_path

    mp4_path = video_path.with_suffix(".mp4")
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        return video_path

    fps = capture.get(cv2.CAP_PROP_FPS) or 25
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(str(mp4_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    while True:
        ok, frame = capture.read()
        if not ok:
            break
        writer.write(frame)

    capture.release()
    writer.release()
    return mp4_path if mp4_path.exists() else video_path


def to_static_result_path(path: Path) -> str:
    relative = path.relative_to(WEB_ROOT / "static")
    return url_for("static", filename=relative.as_posix())


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
