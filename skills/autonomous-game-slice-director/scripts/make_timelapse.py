"""Turn progress screenshots into timelapse videos and captioned storyboard sheets.

Screenshots follow Docs/TASK.md section 18:
    Docs/progress/<feature>/<yyyymmdd-HHMMSS>__<short-caption>.png

Examples:
    python scripts/capture/make_timelapse.py --feature character-creation
    python scripts/capture/make_timelapse.py --all
    python scripts/capture/make_timelapse.py --master            # every feature, ordered by time
    python scripts/capture/make_timelapse.py --all --fps 3 --hold-last 2

Output goes to Docs/progress/_out/: <feature>.mp4 and <feature>_storyboard.jpg.
Needs ffmpeg on PATH and Pillow.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp"}


def caption_of(path: Path) -> str:
    stem = path.stem
    stamp, _, caption = stem.partition("__")
    stamp = stamp.replace("-", " ", 1) if "-" in stamp else stamp
    return f"{stamp}  {caption.replace('-', ' ').replace('_', ' ')}".strip()


def font(size: int):
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def frames_for(folder: Path):
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_TYPES)


def render_frames(images, workdir: Path, width: int, captions: bool, feature_label: bool):
    out = []
    f = font(max(18, width // 60))
    for i, src in enumerate(images):
        im = Image.open(src).convert("RGB")
        h = round(im.height * width / im.width)
        im = im.resize((width, h - h % 2), Image.LANCZOS)
        if captions:
            text = caption_of(src)
            if feature_label:
                text = f"[{src.parent.name}]  {text}"
            d = ImageDraw.Draw(im, "RGBA")
            pad = width // 120
            box = d.textbbox((0, 0), text, font=f)
            d.rectangle((0, im.height - (box[3] - box[1]) - 3 * pad, im.width, im.height), fill=(0, 0, 0, 150))
            d.text((2 * pad, im.height - (box[3] - box[1]) - 2 * pad), text, font=f, fill=(255, 255, 255, 235))
        dst = workdir / f"f{i:06d}.jpg"
        im.save(dst, quality=92)
        out.append(dst)
    return out


def encode(frames, target: Path, fps: float, hold_last: float):
    if not frames:
        return False
    listing = frames[0].parent / "list.txt"
    lines = []
    for fr in frames:
        lines.append(f"file '{fr.as_posix()}'\nduration {1.0 / fps:.4f}")
    lines.append(f"file '{frames[-1].as_posix()}'\nduration {max(hold_last, 1.0 / fps):.4f}")
    lines.append(f"file '{frames[-1].as_posix()}'")
    listing.write_text("\n".join(lines), encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
           "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(target)]
    subprocess.run(cmd, check=True)
    return True


def storyboard(images, target: Path, cols: int = 4, thumb_w: int = 480):
    if not images:
        return
    f = font(16)
    thumbs = []
    for src in images:
        im = Image.open(src).convert("RGB")
        h = round(im.height * thumb_w / im.width)
        im = im.resize((thumb_w, h), Image.LANCZOS)
        cell = Image.new("RGB", (thumb_w, h + 44), (18, 18, 22))
        cell.paste(im, (0, 0))
        ImageDraw.Draw(cell).text((8, h + 10), caption_of(src)[:70], font=f, fill=(230, 230, 230))
        thumbs.append(cell)
    cell_h = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * 8, rows * cell_h + (rows + 1) * 8), (10, 10, 12))
    for i, t in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(t, (8 + c * (thumb_w + 8), 8 + r * (cell_h + 8)))
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, quality=88)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="Docs/progress", help="progress root folder")
    ap.add_argument("--feature", action="append", help="feature folder name (repeatable)")
    ap.add_argument("--all", action="store_true", help="every feature folder")
    ap.add_argument("--master", action="store_true", help="one video of every capture ordered by time")
    ap.add_argument("--fps", type=float, default=3.0, help="frames per second (default 3)")
    ap.add_argument("--hold-last", type=float, default=2.0, help="seconds to hold the last frame")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--no-captions", action="store_true")
    args = ap.parse_args(argv)

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is not on PATH")
    root = Path(args.root)
    out = root / "_out"
    features = []
    if args.all or args.master:
        features = [p for p in sorted(root.iterdir()) if p.is_dir() and p.name not in ("_out",)]
    for name in args.feature or []:
        features.append(root / name)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if args.master:
            everything = sorted((img for folder in features for img in frames_for(folder)), key=lambda p: p.name)
            frames = render_frames(everything, tmp, args.width, not args.no_captions, True)
            if encode(frames, out / "master_timelapse.mp4", args.fps, args.hold_last):
                print("wrote", out / "master_timelapse.mp4", f"({len(frames)} frames)")
            return
        for folder in features:
            images = frames_for(folder)
            if not images:
                continue
            work = tmp / folder.name
            work.mkdir()
            frames = render_frames(images, work, args.width, not args.no_captions, False)
            encode(frames, out / f"{folder.name}.mp4", args.fps, args.hold_last)
            storyboard(images, out / f"{folder.name}_storyboard.jpg")
            print("wrote", out / f"{folder.name}.mp4", f"({len(images)} frames)")


if __name__ == "__main__":
    main()
