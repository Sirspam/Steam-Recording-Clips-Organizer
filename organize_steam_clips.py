import argparse
from datetime import datetime
from pathlib import Path


DEFAULT_PATH = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Utility script to help organise Steam Recording clip files")
    parser.add_argument("-p", "--path", type=Path, default=DEFAULT_PATH, help="Path to Steam Recording clips")
    parser.add_argument("-o", "--output-path", type=Path, help="Path to output organised clips to")
    parser.add_argument("--no-organize", action="store_true", help="Do not organize clips into folders")
    parser.add_argument("--no-24hr-rename", action="store_true", help="Do not convert 12hr file names to 24hr")
    parser.add_argument("--dry-run", action="store_true", help="Print the changes that would be made without actually modifying files")

    return parser.parse_args()


def parse_clip_name(file_path: Path) -> dict | None:
    stem = file_path.stem

    separator_index = stem.rfind(" - ")
    if separator_index == -1:
        return None

    game_title = stem[:separator_index].strip()
    timestamp_text = stem[separator_index + 3:].strip()

    timestamp = None

    for format in ("%Y-%m-%d %I-%M-%S %p", "%Y-%m-%d %H-%M-%S"):
        try:
            timestamp = datetime.strptime(timestamp_text, format)
            break
        except ValueError:
            pass

    if timestamp is None:
        return None

    return {
        "game_title": game_title,
        "timestamp": timestamp,
        "extension": file_path.suffix,
        "original_name": file_path.name,
    }


def build_new_name(parsed_clip: dict) -> str:
    timestamp_24hr = parsed_clip["timestamp"].strftime("%Y-%m-%d %H-%M-%S")
    return f"{parsed_clip['game_title']} - {timestamp_24hr}{parsed_clip['extension']}"


def process_file(file_path: Path, args: argparse.Namespace) -> None:
    parsed_clip = parse_clip_name(file_path)
    if parsed_clip is None:
        print(f"Skipping unrecognised clip name: {file_path.name}")
        return

    new_name = file_path.name
    if not args.no_24hr_rename:
        new_name = build_new_name(parsed_clip)

    destination_path = args.output_path if args.output_path is not None else args.path

    if not args.no_organize:
        destination_path = destination_path / parsed_clip["game_title"]

    destination_path = destination_path / new_name

    if file_path.resolve() == destination_path.resolve():
        print(f"No changes needed: {file_path.name}")
        return

    if destination_path.exists():
        print(f"Skipping because destination already exists: {destination_path}")
        return

    if args.dry_run:
        print(f"Would move: {file_path} -> {destination_path}")
        return

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.rename(destination_path)
    print(f"Moved: {file_path} -> {destination_path}")


def main() -> int:
    args = parse_args()

    if not args.path.exists():
        print(f"Input path does not exist: {args.path}")
        return 1

    if not args.path.is_dir():
        print(f"Input path is not a directory: {args.path}")
        return 1

    if args.output_path is not None:
        args.output_path.mkdir(parents=True, exist_ok=True)

    files = [file for file in args.path.iterdir() if file.is_file() and file.suffix.lower() == ".mp4"]
    if not files:
        print(f"No .mp4 files found in: {args.path}")
    else:
        for file_path in files:
            process_file(file_path, args)

    return 0


if __name__ == "__main__":        
    raise SystemExit(main())